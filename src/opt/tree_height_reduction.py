def run(graph):
	for ID,node in graph.nodes.items():
		if not node.visited and node.type_string == 'opadd':
			worklist = []
			bottom = node
			visit(node, worklist, bottom)
			bottom_width = 0
			for edge in bottom.out_edges:
				if edge.width > bottom_width:
					bottom_width = edge.width
			for work_node in worklist:
				if work_node != bottom and work_node.out_edges[0].width != bottom_width:
					print('removing')
					worklist.remove(work_node)
					work_node.visited = False
			if len(worklist)>2:
				print('nestled loops found')
		else:
			node.visited = True


def visit(node, worklist, bottom):

	if not node.visited:
		#print('appending vertex :'+node.ID)
		node.visited = True
		worklist.append(node)
		to_visit = None
		other_outputs = False
		for pred in node.in_edges:
			node2 = pred.tail
			if node2.type_string == 'opadd':
				#print(node.ID +' calling visit to input edge')
				visit(node2, worklist, bottom)

		for succ in node.out_edges:
			node2 = succ.head
			if node2.type_string == 'opadd':
				if to_visit == None:
					#print('found one to visit')
					to_visit = node2
				else:
					#print('found multiple adds')
					to_visit = None
					break
			else:
				#print('found other outputs')
				other_outputs = True

		if to_visit != None and not other_outputs:
			#print(node.ID +' visiting new out vertex')
			bottom = to_visit
			visit(bottom, worklist, bottom)
		elif (node != bottom):
			worklist.remove(node)
	

	#else:
		#print(node.ID +'already visited')



