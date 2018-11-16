import Node
# class to hold information about dfg
# SCOPE: (We currently assume)
# digraph
# 1 attrib statement node = [shape=record];
# only nodes and edges
# 

class Graph:
	nodes = {}
	edges = []


	def __init__(self, file=None):
		if file != None:
			self.read_from_file(file)


	def read_from_file(self, file):
		for line in file:
				if line.startswith('digraph'):
					continue
				elif line.startswith('}'):
					continue
				elif line.startswith('node'):
					# We are ignoring attr_stmts, should we handle those?
					continue
				elif line == '\n':
					continue
				elif '->' in line:
					self.edge(line)
				else: # assume node
					self.node(line)


	def edge(self, line):
		# TODO order edges by head/tail
		self.edges.append(line)
		return

	def node(self, line):
		node = Node.Node(line)
		if node.ID in self.nodes:
			print('ERROR: Node ID\'s are not unique!')
			exit(-1)
		self.nodes[node.ID] = node
		#print(node.type_string)

	def remove(self, node):
		# TODO remove edges as well!
		self.nodes.pop(node.ID)

	def write_to_file(self, file):
		print("TODO implement Graph.write_to_file")
		file.write('digraph packetarc {\n')
		file.write('node [shape=record];\n')
		for node in self.nodes.values():
			file.write(node.dot_output())
		for edge in self.edges:
			file.write(edge)
		file.write('}')