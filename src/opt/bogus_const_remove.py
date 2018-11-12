# bogus example that removes constant nodes from graph
# only used as example

def run(graph):
	for node in graph.nodes():
		print(node.name())
		print(node.type())
		if(node.type == Node.constant):
			node.remove()
	return graph