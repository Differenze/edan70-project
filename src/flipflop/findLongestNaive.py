map = {}
def run(graph):
	for ID,node in graph.nodes.items():
		if node.label[:5] == 'input':
			print('inputCell found')
			tup = getLongest(node)
			for nod in tup[1]:
				print(nod.ID)


def getLongest(node):
	global size
	max = 1
	path = [node]
	for edge in node.out_edges:
		succ = edge.head
		if succ in map:
			tup = map[succ]
		else:
			tup = getLongest(succ)
			map[succ] = tup
		if tup[0] > max-1:
			max = tup[0]+1
			path = tup[1]
			path.append(node)
	return (max, path)