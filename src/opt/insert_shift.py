def run(graph):
	for ID,node in graph.nodes.items():
		if node.type_string != 'opmul':
			continue
		for edge in node.in_edges:
			if edge.tail.is_constant():
				print(edge.tail.constant_value())
	return graph