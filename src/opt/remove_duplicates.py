

def run(graph):
	for ID,node in graph.nodes.items():
		for ID2,node2 in graph.nodes.items():
			if (ID != ID2 and node.equals(node2)):
				print("found duplicate")
	return graph