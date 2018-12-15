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
		self.label = pydot_node.get_label()

	def add_succ(self, edge):
		self.out_edges.append(edge)
		#print("add_succ:", str(self), str(edge), len(self.out_edges))

	def add_pred(self, edge):
		self.in_edges.append(edge)
		#print("add_pred:", str(self), str(edge), len(self.in_edges))


	def __str__(self):
		return 'Node: %(ID)s %(type_s)s' % ({'ID':self.ID, 'type_s':self.type_string, 'pydot':self.pydot_node})

	def input_edges(self):
		return self.in_edges;

	def left_edge(self):
		for edge in self.in_edges:
			if edge.head_pos == 'left':
				return edge;

	def right_edge(self):
		for edge in self.in_edges:
			if edge.head_pos == 'right':
				return edge;

	def is_constant(self):
		return self.type_string == 'c'


	# returns value if this node is a constant
	def constant_value(self):
		if self.is_constant():
			return int(self.label[1:-1])
		else:
			print('ERR calling constant_value on a node which isn\'t constant')


	def output_nodes(self):
		ret = []
		for edge in self.out_edges:
			ret.append(edge.head)
		return ret

	def output_edges(self):
		return self.out_edges

	# use instead of pydot_node.to_string() because we need to order our outputs
	def dot_string(self):
		node = self.ID
		attr_list = ['label', 'shape', 'color', 'style', 'debug']
		node_attr = []

		for attr in attr_list:
			if attr in self.pydot_node.obj_dict['attributes']:
				value = self.pydot_node.obj_dict['attributes'][attr]
				if value == '':
					value = '""'
				if value is not None:
					node_attr.append('%s=%s' % (attr, pydot.quote_if_necessary(value)))


		node_attr = ' '.join(node_attr)
		if node_attr:
			node += ' [' + node_attr + ']'
		return node + ';'


#		def to_string(self):
#        """Return string representation of node in DOT language."""
#
#
#        # RMF: special case defaults for node, edge and graph properties.
#        #
#        node = quote_if_necessary(self.obj_dict['name'])
#
#        node_attr = list()
#
#        for attr in self.obj_dict['attributes']:
#            value = self.obj_dict['attributes'][attr]
#            if value == '':
#                value = '""'
#            if value is not None:
#                node_attr.append(
#                    '%s=%s' % (attr, quote_if_necessary(value) ) )
#            else:
#                node_attr.append( attr )
#
#
#        # No point in having nodes setting any defaults if the don't set
#        # any attributes...
#        #
#        if node in ('graph', 'node', 'edge') and len(node_attr) == 0:
#            return ''
#
#        node_attr = ', '.join(node_attr)
#
#        if node_attr:
#            node += ' [' + node_attr + ']'
#
#		return node + ';'

