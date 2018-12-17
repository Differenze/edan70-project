def run(graph):
	for ID,node in graph.nodes.items():
		if node.type_string != 'opadd':
			continue
		if node.in_edges[0].tail.type_string == 'opadd' and node.in_edges[1].tail.type_string != 'opadd':
			if node.in_edges[0].tail.in_edges[0].tail.type_string == 'opadd' and node.in_edges[0].tail.in_edges[1].tail.type_string != 'opadd':
				print('found nestled adds')
			elif node.in_edges[0].tail.in_edges[0].tail.type_string != 'opadd' and node.in_edges[0].tail.in_edges[1].tail.type_string == 'opadd':
				print('found nestled adds')
		elif node.in_edges[1].tail.type_string == 'opadd' and node.in_edges[0].tail.type_string != 'opadd':
			if node.in_edges[1].tail.in_edges[0].tail.type_string == 'opadd' and node.in_edges[1].tail.in_edges[1].tail.type_string != 'opadd':
				print('found nestled adds')
			elif node.in_edges[1].tail.in_edges[0].tail.type_string != 'opadd' and node.in_edges[1].tail.in_edges[1].tail.type_string == 'opadd':
				print('found nestled adds')
	return graph
