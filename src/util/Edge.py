import regex as re
import pydot
# Node 		tail
# Node 		head
# int 		width 		(use set_width to update)
# str 		tail_pos	where the edge is anchored on the tail side
# str 		head_pos	where the edge is anchored on the head side
# dict 		obj_dict 	used to create dot_string representation, needs refactor

# An Edge connects tail->head
class Edge:

	# constructor for an Edge
	def __init__(self, tail, head, width, tail_pos=None, head_pos=None, pydot_edge=None):
		self.tail = tail 					# Node object
		self.head = head 					# Node object
		self.width = width 					# how many bits wide the Edge is
		self.tail_pos = tail_pos 			# where the Edge is anchored 
											# on the tail side, e.g. "out"
		self.head_pos = head_pos 			# where the Edge is anchored 
											# on the head side, e.g. "left"
		
		# obj_dict is legacy from using pydot
		self.obj_dict = {} 					# stores all edge data
		self.obj_dict['attributes'] = {} 	# stores edge attributes
		self.obj_dict['attributes']['label'] = '"<'+str(width)+'>"'	
		tail.add_succ(self)
		head.add_pred(self)
		# if this edge is part of a copy of another graph
		# reference_edge will point to the corresponding
		# edge in the original graph
		self.reference_edge = None

	# creates a new Edge from a pydot.Edge
	@staticmethod
	def new_from_pydot(pydot_edge, nodes):
		tail = pydot_edge.get_source().split(':')
		head = pydot_edge.get_destination().split(':')
		tail_pos = None
		head_pos = None
		tail_ID = tail[0]
		if len(tail) > 1:
			tail_pos = tail[1]
		head_ID = head[0]
		if len(head) > 1:
			head_pos = head[1]
		tail = nodes[tail_ID]
		head = nodes[head_ID]
		width = int(pydot_edge.get_label()[2:-2])
		edge = Edge(tail, head, width, tail_pos, head_pos, pydot_edge)
		edge.obj_dict = pydot_edge.obj_dict
		return edge


	# c_10->opadd_11:right[label="<4>"];
	@staticmethod
	def new_from_string(dot_string, nodes):
		edge, attrib = dot_string.split('[')
		attrib.rstrip('];\n')
		match=re.search('label="(.*?)"', attrib)
		label=match.group(1)
		# print(dot_string, label)
		width=int(label[1:-1])

		tail, head = edge.split('->')
		tail_pos = None 
		head_pos = None
		if ':' in tail:
			tail, tail_pos = tail.split(':')
		if ':' in head:
			head, head_pos = head.split(':')

		tail = nodes[tail]
		head = nodes[head]

		edge = Edge(tail, head, width, tail_pos, head_pos, None)
		return edge


	# needs refactoring, the obj_dict is legacy from using pydot
	# returns string representation of this Edge on the dot format
	def dot_string(self):
		edge = []
		edge.append(self.tail.ID)
		if(self.tail_pos):
			edge.append(':'+self.tail_pos)
		edge.append('->')
		edge.append(self.head.ID)
		if(self.head_pos):
			edge.append(':'+self.head_pos)

		# the order in which attributes are appended is important for pacopt
		# therefore the pydot library could not be used, excuse the following hacks
		attr_list = ['label', 'debug']
		edge_attr = []

		for attr in attr_list:
			if attr in self.obj_dict['attributes']:
				value = self.obj_dict['attributes'][attr]
				if value == '':
					value = '""'
				if value is not None:
					edge_attr.append('%s=%s' % (attr, pydot.quote_if_necessary(value)))

		edge_attr = ', '.join(edge_attr)

		if edge_attr:
			edge.append('[' + edge_attr + ']')

		return ''.join(edge) + ';'

	# updates the width of this Edge
	def set_width(self, number):
		self.width = number
		self.obj_dict['attributes']['label'] = '"<'+str(number)+'>"'

	# used by flipflop.nodemerging
	def __lt__(self, other):
		return self.width<other.width

	# string representation for printouts
	def __str__(self):
		return 'Edge: %(tail)s <%(width)s>-> %(head)s' % ({'tail':self.tail, 'head':self.head, 'width':self.width})