from util.Graph import Graph
import argparse
import sys
import copy


import opt.eq_1 as eq_1
import opt.remove_duplicates as remove_duplicates
import opt.insert_shift as insert_shift
import opt.const_merging as const_merging
import opt.alg_simp as alg_simp
import opt.tree_height_red as tree_height_red
import opt.bitwidth as bitwidth

import flipflop.greedy as greedy
import flipflop.printout as printout
import flipflop.remff as remff
import flipflop.calcFF as calcFF
import flipflop.findLongestNaive as findLongestNaive

# use:
# python src/optimize.py -h
# for help on how to use this


parser=argparse.ArgumentParser()
# input file argument
parser.add_argument('infile', 
	metavar='input.dot', 
	type=argparse.FileType('r'), 
	help='input file to be optimized')
# output file argument defaults to "output.dot"
parser.add_argument(
	'-o',
	'--outfile', 
	metavar='output.dot', 
	type=argparse.FileType('w'),
	default=open('output.dot','w'), 
	help='output file, output.dot by default', 
	nargs=1)

# arguments for each optimization
parser.add_argument('--all', action='store_true', help='apply all optimizations')
parser.add_argument('--eq_1', action='store_true', help='removes 1 bit nodes where output is equal to input')
parser.add_argument('--remove_duplicates', action='store_true', help='removes nodes which perform the same operation with different input')
#parser.add_argument('--in_shift', action='store_true', help='[not implemented] replaces multiplications with shift operations')
parser.add_argument('--const_merging', action='store_true', help='merges additions/subtractions with constants')
#parser.add_argument('--alg_simp', action='store_true', help='[not implemented] simplifies algebraic expression')
parser.add_argument('--bitwidth', action='store_true', help='removes insignificant bits')
parser.add_argument('--tree_height_red_add', action='store_true', help='balances trees of add/sub operations')
parser.add_argument('--tree_height_red_and', action='store_true', help='balances trees of and operations')
parser.add_argument('--tree_height_red_or', action='store_true', help='balances trees of or operations')
parser.add_argument('--greedy', action='store_true', help='greedy insertion of flip flops')
parser.add_argument('--printout', action='store_true', help='print debug info')
parser.add_argument('--remff', action='store_true', help='creates a second graph with flip flops removed (reset the result from pacopt)')
parser.add_argument('--calcFF', action='store_true', help='calculates total width of the flipflops')
parser.add_argument('--findLongestNaive', action='store_true', help='finds the longest path')

args=parser.parse_args()
	
print('parsing graph')
graph = Graph(args.infile)
original_graph = copy.deepcopy(graph)
# run the selected optimizations (order matters):

if(args.all or args.bitwidth):
	print('start bitwidth optimization')
	bitwidth.run(graph)

if(args.all or args.eq_1):
	print('start eq_1 optimization')
	eq_1.run(graph)

if(args.all or args.remove_duplicates):
	print('start remove_duplicates optimization')
	remove_duplicates.run(graph)

# Not implemented due to feasibility 
# if(args.all or args.in_shift):
# 	print('start insert shift optimization')
# 	insert_shift.run(graph)

if(args.all or args.const_merging):
	print('start const_merging optimization')
	const_merging.run(graph)

# Not implemented due to feasibility
# if(args.all or args.alg_simp):
# 	print('start algebraic simplification optimization')
# 	alg_simp.run(graph)

if(args.all or args.tree_height_red_add):
	print('start tree height reduction add/sub optimization')
	tree_height_red.run(graph, 'add')

if(args.all or args.tree_height_red_and):
	print('start tree height reduction and optimization')
	tree_height_red.run(graph, 'and')

if(args.all or args.tree_height_red_or):
	print('start tree height reduction or optimization')
	tree_height_red.run(graph, 'or')


## Project 2 graph splitting optimization starts here

# TODO make sure this is run for the ones who require it to be done
if(args.remff):
	print('removing flip flops from graph')
	remff.run(graph)

if(args.greedy):
	print('start greedy flip flop insertion')
	greedy.run(graph)

if(args.printout):
	print('start debug print')
	printout.run(graph)
if(args.calcFF):
	print('start calcFF')
	calcFF.run(graph)
if(args.findLongestNaive):
	print('start find longest naive')
	findLongestNaive.run(graph)

# write output graph to file
print('writing to file:', args.outfile)
graph.write_to_file(args.outfile)
# original_graph.write_to_file(args.outfile+"unchanged")