from util.Graph import Graph
import argparse
import sys

possible_opts=['bogus_const_remove', '...']
import opt.bogus_const_remove



# Code to add command line arguments
parser=argparse.ArgumentParser()
parser.add_argument('infile', 
	metavar='input.dot', 
	type=file, 
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
print(opts)
if(not opts):
	print('user asked for no optimizations, output identical to input')
	# TODO output unchanged graph (could be useful for scripting)
	exit(0)

print('parsing graph')
graph = Graph(args.infile)
if('test_opt1' in opts):
	print('start test optimization 1')
	graph = opt.bogus_const_remove.run(graph)

if('test_opt2' in opts):
	print('start test optimization 2')
	#graph = testopt2(graph)

graph.write_to_file(args.outfile)