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
	nodes = {}
	edges = []
	pydot_graph = None

	def __init__(self, file=None):
		if file != None:
			self.read_from_file(file)
		else:
			print("TODO allow creating empty graph")


	def read_from_file(self, file):
		file.close()
		self.pydot_graph = pydot.graph_from_dot_file(file.name)[0]
		for node in self.pydot_graph.get_node_list():
			self.node(node)
		for edge in self.pydot_graph.get_edge_list():
			self.edge(edge)



	def edge(self, pydot_edge):
		# TODO order edges by head/tail
		edge = Edge.new_from_pydot(pydot_edge, self.nodes)
		self.edges.append(edge)


	def node(self, pydot_node):
		if pydot_node.get_name() == 'node':
			return;
		node = Node.new_node_from_pydot(pydot_node)
		if node.ID in self.nodes:
			print(node.ID)
			print(self.nodes[node.ID].ID)
			print('ERROR: Node ID\'s are not unique!:', str(node), str(self.nodes[node.ID]))
			exit(-1)
		self.nodes[node.ID] = node
		#print(node.type_string)


	def remove_node(self, node):
		#print('removing:', str(node.pydot_node))
		for edge in node.out_edges+node.in_edges:
			self.remove_edge(edge)
		self.nodes.pop(node.ID)

	def remove_edge(self, edge):
		#print('removing:', str(edge.pydot_edge))
		if edge in self.edges:
			# remove edge from successor and predecessor
			# TODO check that they exist maybe?
			edge.head.in_edges.remove(edge)
			edge.tail.out_edges.remove(edge)
			self.edges.remove(edge)
			return
		else:
			print('edge not in graph_edges', edge.pydot_edge.get_source(), edge.pydot_edge.get_destination())

	def write_to_file(self, file):
		#file.close()
		#self.pydot_graph.write(file.name)
		file.write('digraph packetarc {\n')
		file.write('node [shape=record];\n')
		for node in self.nodes.values():
			file.write(node.dot_string() + '\n')
		for edge in self.edges:
			file.write(edge.dot_string() + '\n')
		file.write('}\n')


	def create_edge(self, tail, head, width, tail_pos=None, head_pos=None, pydot_edge=None):
		edge = Edge(tail, head, width, tail_pos, head_pos)
		print('creating edge:', str(edge))
		print(edge.dot_string())
		self.edges.append(edge)
		#self.pydot_graph.add_edge(edge.pydot_edge)

	def create_node(self, type_string):
		node = Node(type_string)
		if node.ID in self.nodes:
			print(node.ID)
			print(self.nodes[node.ID].ID)
			print('ERROR: Node ID\'s are not unique!:', str(node), str(self.nodes[node.ID]))
			exit(-1)
		self.nodes[node.ID] = node
		return node
