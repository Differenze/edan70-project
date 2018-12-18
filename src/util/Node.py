import pydot
# str 			ID 				what this node is called
# [Edge]		out_edges 		edges leaving this node
# [Edge]		in_edges 		edges entering this node
# str 			type_string		what type is this node, e.g. ADD/SUB/C

DEFAULT_LABELS = {
	'opadd' : '{{<left> left | <right> right} | <out> add}',
	'opsub' : '{{<left> left | <right> right} | <out> sub}',
	'c'		: 'USE Graph.create_constant for sane defaults'
}

class Node:
	MAX_ID = 0

	def __init__(self, type_string, ID=None, label=None):
		self.visited = False 
		self.out_edges = []
		self.in_edges = []
		self.ID = ID
		if not ID:
			Node.MAX_ID += 1
			self.ID = type_string+'_'+str(Node.MAX_ID)
		self.type_string = type_string
		self.label = label
		if not label:
			if type_string not in DEFAULT_LABELS:
				print("No default label found for this type: ", type_string) # look at type_string and use a default?
				exit(-1)
			self.label = DEFAULT_LABELS[type_string]
		self.obj_dict = {}
		self.obj_dict['attributes'] = {}
		self.obj_dict['attributes']['label'] = self.label


	@staticmethod
	def new_node_from_pydot(pydot_node):
		ID = pydot_node.get_name()
		type_string = "".join(pydot_node.get_name().split('_')[:-1])
		label = pydot_node.get_label()
		node = Node(type_string, ID, label)
		node.obj_dict = pydot_node.obj_dict
		idnum = int(ID.split('_')[1:][0])
		if idnum > Node.MAX_ID:
			Node.MAX_ID = idnum
		return node

	def add_succ(self, edge):
		self.out_edges.append(edge)
		#print("add_succ:", str(self), str(edge), len(self.out_edges))

	def add_pred(self, edge):
		self.in_edges.append(edge)
		#print("add_pred:", str(self), str(edge), len(self.in_edges))


	def __str__(self):
		return 'Node: %(ID)s %(type_s)s %(label)s' % ({'ID':self.ID, 'type_s':self.type_string, 'label':self.label})

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


	# returns nodes which are behind self
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
			if attr in self.obj_dict['attributes']:
				value = self.obj_dict['attributes'][attr]
				if value == '':
					value = '""'
				if value is not None:
					node_attr.append('%s=%s' % (attr, pydot.quote_if_necessary(value)))


		node_attr = ' '.join(node_attr)
		if node_attr:
			node += ' [' + node_attr + ']'
		return node + ';'

	def set_label(self, value):
		self.label=value
		self.set_attrib('label', value)
	def set_attrib(self, attrib, value):
		self.obj_dict['attributes'][attrib] = value

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

