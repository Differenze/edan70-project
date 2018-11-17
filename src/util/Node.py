import pydot

class Node:

	def __init__(self, pydot_node=None):
		self.out_edges = []
		self.in_edges = []
		if pydot_node:
			self.parse(pydot_node)
		else:
			# TODO allow creating new node
			print('TODO allow creating node without pydot_node')


	def parse(self, pydot_node):
		self.pydot_node = pydot_node
		self.ID = pydot_node.get_name()
		self.type_string = "".join(pydot_node.get_name().split('_')[:-1])


	def add_succ(self, edge):
		self.out_edges.append(edge)
		#print("add_succ:", str(self), str(edge), len(self.out_edges))

	def add_pred(self, edge):
		self.in_edges.append(edge)
		#print("add_pred:", str(self), str(edge), len(self.in_edges))


	def __str__(self):
		return 'Node: %(ID)s %(type_s)s' % ({'ID':self.ID, 'type_s':self.type_string, 'pydot':self.pydot_node})