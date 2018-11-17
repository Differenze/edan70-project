from util.Graph import Graph
import argparse
import sys

possible_opts=['bogus_const_remove', '...']
import opt.bogus_const_remove as bogus_const_remove



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
#print args



opts = args.opts
print('parsing graph')
graph = Graph(args.infile)

if(not opts):
	print('user asked for no optimizations, output identical to input')
	graph.write_to_file(args.outfile)
	exit(0)

if('bogus_const_remove' in opts):
	print('start bogus optimization 1')
	graph = bogus_const_remove.run(graph)

if('test_opt2' in opts):
	print('start test optimization 2')
	#graph = testopt2(graph)

graph.write_to_file(args.outfile)