def run(graph, unchanged_graph):
	graph_sum = 0
	unchanged_sum = 0

	for node in graph.nodes.values():
		if node.type_string == 'ff':
			width = int(node.info["width"])
			graph_sum += width
	
	for node in unchanged_graph.nodes.values():
		if node.type_string == 'ff':
			width = int(node.info["width"])
			unchanged_sum += width
		

	print("Unchanged graph costs {} flipflops".format(unchanged_sum))
	print("Modified graph costs {} flipflops".format(graph_sum))