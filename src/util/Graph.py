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


	def node(self, pydot_edge):
		node = Node(pydot_edge)
		if node.ID in self.nodes:
			print('ERROR: Node ID\'s are not unique!:', node, self.nodes[node.ID])
			exit(-1)
		self.nodes[node.ID] = node
		#print(node.type_string)

	def remove_node(self, node):
		print('removing:', str(node.pydot_node))
		for edge in node.out_edges+node.in_edges:
			self.remove_edge(edge)
		self.pydot_graph.del_node(node.ID)
		self.nodes.pop(node.ID)

	def remove_edge(self, edge):
		print('removing:', str(edge.pydot_edge))
		if self.pydot_graph.del_edge(edge.pydot_edge.get_source(), edge.pydot_edge.get_destination()):
			return
		else:
			print('could not delete:', edge.pydot_edge.get_source(), edge.pydot_edge.get_destination())
		# TODO? self.edges.remove(edge)

	def write_to_file(self, file):
		file.close()
		self.pydot_graph.write(file.name)


	def create_edge(self, tail, head, width, tail_pos=None, head_pos=None, pydot_edge=None):
		edge = Edge(tail, head, width, tail_pos, head_pos)
		print('creating edge:', str(edge))
		print(edge.pydot_edge)
		self.edges.append(edge)
		self.pydot_graph.add_edge(edge.pydot_edge)