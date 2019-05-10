def run(graph):
	sum = 0
	sumlarge = 0
	for ID,node in graph.nodes.items():
		if node.type_string == 'ff':
			#if(ID == 'ff_1'):
			#	sumlarge = sumLarge(node)
			width = int(node.info["width"])
			sum += width
			if width >= 1200:
				sumlarge += 1280
		

	print(sum)
	print(sumlarge)

def sumLarge(node):
	width = node.info["width"]
	amount = 1
	next = node.out_edges[0].head
	while(node.type_string == 'ff'):
		if (node.info["width"] != width):
			print("Error, wrong width")
		else:
			amount += 1
		if len(next.out_edges)>0:
			next = next.out_edges[0].head
		else: 
			break
	return int(width)*amount