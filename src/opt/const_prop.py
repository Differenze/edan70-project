# finds chains of calculations with constants

from util.Node import Node

arithmetics = ['opadd', 'opsub'] # maybe this could be extended to use mul/and/or/...
CONST = 'c'

def run(graph):
	for ID,node in graph.nodes.items():
		if is_const_arithm(node):
			for edge in node.output_edges():
				successor = edge.head
				if is_const_arithm(successor):
					# we have two nodes following each other which both are additions/subtraction with constants
					summ = 0
					summ += aritmvalue(node)
					summ += aritmvalue(successor)
					replace_nodes(node, successor, summ)
					


def replace_nodes(node1, node2, summ):
	print(node1)
	if summ < 0:
		sub_node = Node()
	if summ > 0:
		insert_add()
	if summ == 0:
		remove_tree()






# node = this node
# cped = predecessor of this node which is constant
def aritmvalue(node):
	cval = None
	if node.left_edge().tail.is_constant():
		cval = node.left_edge().tail.constant_value()
		if cval == None:
			print('Whit')
	if node.right_edge().tail.is_constant():
		cval = node.right_edge().tail.constant_value()
		if cval == None:
			print('What')

	if node.type_string == 'opsub':
		return -cval
	return cval


def is_const_arithm(node):
	if node.type_string in arithmetics:
		# we assume that only left or right is constant		
		if node.left_edge().tail.is_constant():
			return node.left_edge().tail
		if node.right_edge().tail.is_constant():
			return node.right_edge().tail
	return False
