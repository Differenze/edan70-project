def run(graph):
	worklist = graph.nodes.values()
	while worklist:
		node = worklist.pop()
		print(node.label)
