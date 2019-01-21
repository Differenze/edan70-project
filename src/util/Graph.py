from util.Node import Node
from util.Edge import Edge
import regex as re
import pydot
# class to hold information about dfg
# SCOPE: (We currently assume)
# digraph
# 1 attrib statement node = [shape=record];
# only nodes and edges
# 

class Graph:
	nodes = {} # all nodes in the graph, ordered by ID
	edges = [] # all edges in the graph
	pydot_graph = None


	# constructs a graph
	def __init__(self, file=None):
		if file != None:
			self.read_from_file(file)
		else:
			# TODO if necessary
			print("TODO allow creating empty graph")


	# reads a graph from a file using the pydot library
	def read_from_file(self, file):
		file.close()
		print(file.name)
		self.pydot_graph = pydot.graph_from_dot_file(file.name)[0]
		for node in self.pydot_graph.get_node_list():
			self.node(node)
		for edge in self.pydot_graph.get_edge_list():
			self.edge(edge)


	# creates an Edge object from a pydot.Edge
	def edge(self, pydot_edge):
		edge = Edge.new_from_pydot(pydot_edge, self.nodes)
		self.edges.append(edge)


	# creates a Node object from a pydot.Node
	def node(self, pydot_node):
		# catches the first line which defines node shape/color
		if pydot_node.get_name() == 'node':
			return
		node = Node.new_node_from_pydot(pydot_node)
		if node.ID in self.nodes:
			print(node.ID)
			print(self.nodes[node.ID].ID)
			print('ERROR: Node ID\'s are not unique!:', str(node), str(self.nodes[node.ID]))
			exit(-1)
		self.nodes[node.ID] = node


	def remove_node(self, node):
		for edge in node.out_edges+node.in_edges:
			self.remove_edge(edge)
		self.nodes.pop(node.ID)


	def remove_edge(self, edge):
		if edge in self.edges:
			# remove edge from successor and predecessor
			edge.head.in_edges.remove(edge)
			edge.tail.out_edges.remove(edge)
			self.edges.remove(edge)
			return
		else:
			print('edge not in graph_edges', edge.pydot_edge.get_source(), edge.pydot_edge.get_destination())


	# writes the graph into a file using the dot format
	def write_to_file(self, file):
		file.write('digraph packetarc {\n')
		file.write('node [shape=record];\n')
		for node in self.nodes.values():
			file.write(node.dot_string() + '\n')
		for edge in self.edges:
			file.write(edge.dot_string() + '\n')
		file.write('}\n')


	# create a new edge in this graph
	def create_edge(self, tail, head, width, tail_pos=None, head_pos=None, pydot_edge=None):
		edge = Edge(tail, head, width, tail_pos, head_pos)
		self.edges.append(edge)


	# create a new node in this graph
	def create_node(self, type_string):
		node = Node(type_string)
		if node.ID in self.nodes:
			print('ERROR: Node ID\'s are not unique!:', str(node), str(self.nodes[node.ID]))
			exit(-1)
		self.nodes[node.ID] = node
		return node


	# create a constant node with given value
	# c_128 [label="0" shape=plaintext color="red" style="filled"];
	def create_constant(self, value):
		node = self.create_node('c')
		node.set_label('"'+str(value)+'"')
		node.set_attrib('shape', 'plaintext')
		node.set_attrib('color', 'red')
		node.set_attrib('style', 'filled')
		return node