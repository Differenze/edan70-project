import util.Edge as Edge

# Searches through the graph to find duplicate operations. 
# Such instances are found by looking to see if the operations have the same input. 
# This could e expanded upon by evaulatng whether they instead have "equivalent" inputs, i.e some form of constant propagation would be needed.

def run(graph):
	remove_duplicate(graph)
	return graph

#returns true if a duplicate was removed, else false
def remove_duplicate(graph):
	worklist = []
	for ID,node1 in graph.nodes.items():
		# bitconcats have a lot of inputs and therefore take a long time to process, they also have a sze of zero so they are not relevant to this optimization. 
		# Please note that several bitconcats can however be safely removed, if this proves beneficial for other purposes.
		if (len(node1.in_edges)>20 and node1.type_string == 'bitconcat'):
			continue
		for pred in node1.in_edges:
			for succ in pred.tail.out_edges:
				node2 = succ.head
				if (node_equals(node1,node2) and ID in graph.nodes.keys() and node2.ID in graph.nodes.keys() and node1 != node2):
					if(node1.type_string not in ["out" , "in", 'c']):
						print("duplicate found with ID1: "+ID)
						#replacing edges
						for edge2 in node2.out_edges:
							edge1 = graph.create_edge(node1, edge2.head, edge2.width, edge2.head_pos)
							worklist.append(edge2.head)
						graph.remove_node(node2)

	while worklist:	
		node = worklist.pop()
		if (len(node.in_edges)>20 and node.type_string == 'bitconcat'):
			continue
		for pred in node.in_edges:
			for succ in pred.tail.out_edges:
				node2 = succ.head
				if (node_equals(node1,node2) and ID in graph.nodes.keys() and node2.ID in graph.nodes.keys() and node1 != node2):
					if(node1.type_string not in ["out" , "in", 'c']):
						print("duplicate found with ID1: "+ID)
						#replacing edges
						for edge2 in node2.out_edges:
							edge1 = graph.create_edge(node1, edge2.head, edge2.width, edge2.head_pos)
							worklist.append(edge2.head)
						graph.remove_node(node2)

			

	

#returns true if both nodes always have the same output
def node_equals(node1, node2):
	
	if (node1.type_string != node2.type_string):
		return False

	for edge1 in node1.in_edges:
		found = False
		for edge2 in node2.in_edges:
			if edge_equals(edge1,edge2):
				found = True
				break
		if not found:
			return False
	return True

#returns true if both edges are equal for two different nodes
def edge_equals(edge1, edge2):
	if (edge1.tail != edge2.tail):
		return False
	if (edge1.width != edge2.width):
		return False
	if (edge1.tail_pos != edge2.tail_pos):
		return False
	if (edge1.head_pos != edge2.head_pos):
		return False
	return True