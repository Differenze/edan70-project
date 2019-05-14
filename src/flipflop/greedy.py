
def run(graph):
	worklist = graph.nodes.values()
	node = worklist.pop()
	node = worklist.pop()
	node = worklist.pop()
	print(node.label)	
	node.insertFF(graph)
