import util.Edge as Edge

def run(graph):
	remove_duplicate(graph)
	return graph

#returns true if a duplicate was removed, else false
def remove_duplicate(graph):
	for ID,node1 in graph.nodes.items():
		for ID2,node2 in graph.nodes.items():
			if (ID in graph.nodes.keys() and ID2 in graph.nodes.keys() and ID != ID2 and node_equals(node1,node2)):
				if(node1.type_string not in ["out" , "in", 'c']):
					print("duplicate found with ID1: "+ID+", ID2: ", ID2)
					#replacing edges
					for edge2 in node2.out_edges:
						edge1 = Edge.Edge(node1, edge2.head, edge2.width, None, edge2.head_pos, None)
						print("adding succ")
						node1.add_succ(edge1)
						graph.edges.append(edge1)
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