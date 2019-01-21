# Searches for miltiplications or divisions by a multiple of 2, for an easy way of evaulating if these could be replaced by a bitshift. 
# However only one such case exicts so the optimization was deemed not relevant to these instances.
# Note that the actual implementation would look for values of a power of two.

def run(graph):
	for ID,node in graph.nodes.items():
		if node.type_string not in ['opmul', 'opdiv']:
			continue
		for edge in node.in_edges:
			if edge.tail.is_constant():
				if (edge.tail.constant_value() % 2 == 0):
					print(edge.tail.constant_value())
	return graph