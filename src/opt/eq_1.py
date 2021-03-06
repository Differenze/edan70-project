# --eq_1
# Removes comparison nodes where a single 
# bit is compared to 0 or 1 when possible.


def run(graph):
	deleted_nodes = 0
	for ID,node in graph.nodes.items():
		if(node.type_string == 'opeq' or node.type_string == 'opne'):
			cval = 1 if node.type_string == 'opeq' else 0
			le = node.left_edge()
			re = node.right_edge()
			if le.width == 1 and re.width == 1:
				if(le.tail.is_constant() and le.tail.constant_value() == cval):
					del_node(re, node, graph)
					deleted_nodes += 1
					if len(le.tail.output_edges()):
						graph.remove_node(le.tail)
				elif(re.tail.is_constant() and re.tail.constant_value() == cval):
					del_node(le, node, graph)
					deleted_nodes += 1
					if len(re.tail.output_edges()):
						graph.remove_node(re.tail)
	# print('Deleted ', deleted_nodes, ' nodes.')
	return graph


def del_node(inp_edge, node, graph):
	inp_node = inp_edge.tail
	for out_edge in node.output_edges():
		out_node = out_edge.head
		graph.create_edge(inp_node, out_node, 1, inp_edge.tail_pos, out_edge.head_pos)
	graph.remove_node(node)
