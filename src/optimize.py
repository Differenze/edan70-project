from util.Graph import Graph
import argparse
import sys


import opt.eq_1 as eq_1
import opt.remove_duplicates as remove_duplicates
import opt.insert_shift as insert_shift
import opt.const_merging as const_merging
import opt.alg_simp as alg_simp
import opt.tree_height_red as tree_height_red


import opt.bitwidth as bitwidth



# Code to add command line arguments
parser=argparse.ArgumentParser()
parser.add_argument('infile', 
	metavar='input.dot', 
	type=argparse.FileType('r'), 
	help='input file to be optimized')
parser.add_argument('outfile', 
	metavar='output.dot', 
	type=argparse.FileType('w'),
	default=open('output.dot','w'), 
	help='output file, output.dot by default', 
	nargs='?')

#parser.add_argument('--opts', help='test', type=str, choices=possible_opts, nargs='+')
parser.add_argument('--all', action='store_true')
parser.add_argument('--eq_1', action='store_true')
parser.add_argument('--remove_duplicates', action='store_true')
parser.add_argument('--in_shift', action='store_true')
parser.add_argument('--const_merging', action='store_true')
parser.add_argument('--alg_simp', action='store_true')
parser.add_argument('--tree_height_red_add', action='store_true')
parser.add_argument('--tree_height_red_and', action='store_true')
parser.add_argument('--tree_height_red_or', action='store_true')
parser.add_argument('--bitwidth', action='store_true')

args=parser.parse_args()

if args.all:
	print('ALL')
	
print('parsing graph')
graph = Graph(args.infile)

if(args.all or args.bitwidth):
	print('start bitwidth optimization')
	bitwidth.run(graph)

if(args.all or args.eq_1):
	print('start eq_1 optimization')
	eq_1.run(graph)

if(args.all or args.remove_duplicates):
	print('start remove_duplicates optimization')
	remove_duplicates.run(graph)

if(args.all or args.in_shift):
	print('starting insert shift optimization')
	insert_shift.run(graph)

if(args.all or args.const_merging):
	print('start const_merging optimization')
	const_merging.run(graph)

if(args.all or args.alg_simp):
	print('starting alebraic simplification optimization')
	alg_simp.run(graph)

if(args.all or args.tree_height_red_add):
	print('starting tree height reduction add optimization')
	tree_height_red.run(graph, 'add')

if(args.all or args.tree_height_red_and):
	print('starting tree height reduction and optimization')
	tree_height_red.run(graph, 'and')

if(args.all or args.tree_height_red_or):
	print('starting tree height reduction or optimization')
	tree_height_red.run(graph, 'or')

print('writing to file:', args.outfile)
graph.write_to_file(args.outfile)