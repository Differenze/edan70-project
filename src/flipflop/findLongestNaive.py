def run(graph):
	for node in graph.nodes.items():
		if node.label[:9] == 'inputCell':
			print node.label
			print node.type_string