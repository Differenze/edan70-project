# Simple prints to identify candidates for simplification, Evaluated to not be worth implementing as such cases do not excist.

def run(graph):
	for ID,node in graph.nodes.items():
		if node.type_string != 'opadd':
			continue
		if node.in_edges[0].tail == node.in_edges[1].tail:
			print('found one!')
		if node.in_edges[0].tail.type_string == 'opmul' and node.in_edges[1].tail.type_string == 'opmul':
			print('found two mul!')
		elif node.in_edges[0].tail.type_string == 'opmul' and node.in_edges[1].tail.type_string == 'opadd' and (node.in_edges[1].tail.in_edges[0].type_string == 'opmul' or node.in_edges[1].tail.in_edges[1].type_string == 'opmul'):
			print('found difficult add muls')
		elif node.in_edges[1].tail.type_string == 'opmul' and node.in_edges[0].tail.type_string == 'opadd' and (node.in_edges[0].tail.in_edges[0].type_string == 'opmul' or node.in_edges[0].tail.in_edges[1].type_string == 'opmul'):
			print('found difficult add muls')
	return graph
