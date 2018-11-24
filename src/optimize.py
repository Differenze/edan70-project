from util.Graph import Graph
import argparse
import sys

possible_opts=['all', 'bogus_const_remove', 'eq_1']
import opt.bogus_const_remove as bogus_const_remove
import opt.eq_1 as eq_1



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

parser.add_argument('--opts', help='test', type=str, choices=possible_opts, nargs='+')

args=parser.parse_args()

opts = args.opts
	
print('parsing graph')
graph = Graph(args.infile)

if(not opts):
	print('user asked for no optimizations, output identical to input')
	graph.write_to_file(args.outfile)
	exit(0)

if 'all' in opts:
	opts = possible_opts

if('bogus_const_remove' in opts):
	print('start bogus optimization 1')
	graph = bogus_const_remove.run(graph)

if('eq_1' in opts):
	print('start eq_1 optimization')
	graph = eq_1.run(graph)

graph.write_to_file(args.outfile)