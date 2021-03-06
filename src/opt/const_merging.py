# --const_merging
# finds chains of arithmetics with constants

import math

arithmetics = ['opadd', 'opsub'] # TODO could this be extended to use mul/and/or/ ?

def run(graph):
	worklist = graph.nodes.values()
	while worklist:
		node = worklist.pop()
		if not node:
			continue
		if is_const_arithm(node):
			for edge in node.output_edges():
				successor = edge.head
				if is_const_arithm(successor):
					# we have two nodes following each other which 
					# both are additions/subtraction with constants
					summ = 0
					summ += aritmvalue(node)
					summ += aritmvalue(successor)
					replace_nodes(node, successor, summ, graph, worklist)

	# remove unused constants
	for ID,node in graph.nodes.items():
		if node.is_constant() and len(node.output_edges())==0:
			graph.remove_node(node)


# calculate bitwidth for a constant number
def bitwidth(number):
	if number == 0:
		return 0
	if number < 0:
		number = -number
	return int(math.floor(math.log(number, 2))+1)


def replace_nodes(node, succ, summ, graph, worklist):
	pred_edge = node.left_edge()
	if node.left_edge().tail.is_constant():
		pred_edge = node.right_edge()

	# TODO fix the width, this underestimates the quality of c_merging
	width = max(pred_edge.width, bitwidth(summ))
	if summ == 0:
		# remove existing nodes
		repl_node = pred_edge.tail
	else:
		if summ < 0:
			#insert subtraction instead of the two existing nodes
			type_string = 'opsub'
			cvalue = -summ
		if summ > 0:
			#insert addition instead of the two existing nodes
			type_string = 'opadd'
			cvalue = summ

		repl_node = graph.create_node(type_string)
		c_node = graph.create_constant(cvalue)
		graph.create_edge(pred_edge.tail, repl_node, width, pred_edge.tail_pos, 'right')
		graph.create_edge(c_node, repl_node, width, None, 'left')
	
	# create new edges in place of the outgoing ones
	for end in list(succ.output_edges()):
		graph.create_edge(repl_node, end.head, width, 'out', end.head_pos)
		graph.remove_edge(end)

	# if the nodes are no longer used, remove them
	if len(succ.output_edges()) == 0:
		graph.remove_node(succ)
	if len(node.output_edges()) == 0:
		graph.remove_node(node)
	worklist.append(repl_node)


# returns the number value that is added by this node
# returns negative values for subtractions
def aritmvalue(node):
	cval = None
	if node.left_edge().tail.is_constant():
		cval = node.left_edge().tail.constant_value()
	if node.right_edge().tail.is_constant():
		cval = node.right_edge().tail.constant_value()

	if node.type_string == 'opsub':
		return -cval
	return cval


# return true if node is an ADD/SUB with a constant value
def is_const_arithm(node):
	if node.type_string in arithmetics:
		if not node.left_edge() or not node.right_edge():
			#this node has very likely been removed from the actual graph allreadey
			return False
		# we assume that only left or right is constant		
		if node.left_edge().tail.is_constant():
			return node.left_edge().tail
		if node.right_edge().tail.is_constant():
			return node.right_edge().tail
	return False
