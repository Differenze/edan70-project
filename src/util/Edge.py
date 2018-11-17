
# 
class Edge:

	#  tail->head
	def __init__(self, tail, head, width, tail_pos=None, head_pos=None, pydot_edge=None):
		self.tail = tail
		self.head = head
		self.width = width
		self.tail_pos = tail_pos
		self.head_pos = head_pos
		self.pydot_edge = pydot_edge
		tail.add_succ(self)
		head.add_pred(self)

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
		width = -1 # TODO!!!
		return Edge(tail, head, width, tail_pos, head_pos, pydot_edge)


	def __str__(self):
		return 'Edge: %(tail)s -> %(head)s' % ({'tail':self.tail, 'head':self.head, 'pydot':self.pydot_edge})