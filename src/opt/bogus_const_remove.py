# bogus example that removes constant nodes from graph
# only used as example

def run(graph):
	for ID,node in graph.nodes.items():
		if(node.type_string == 'c'):
			graph.remove_node(node)
			#return graph
	return graph