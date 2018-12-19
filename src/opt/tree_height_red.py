def run(graph, opt):
	opts = None
	if (opt == 'add'):
		opts = ['opadd', 'opsub']
	elif (opt == 'and'):
		opts = ['opand']
	elif (opt == 'or' ):
		opts = ['opor']

	for ID,node in graph.nodes.items():
		if not node.visited and node.type_string in opts:
			worklist = []
			bottom = node

			bottom = visit(node, worklist, bottom, opts)
			bottom_width = 0
			for edge in bottom.out_edges:
				if edge.width > bottom_width:
					bottom_width = edge.width
			for work_node in worklist:
				if work_node != bottom and work_node.out_edges[0].width != bottom_width:
					#print('removing')
					worklist.remove(work_node)
					work_node.visited = False
			if len(worklist)>2:
				#print('nestled tree found')
				inputlist = []
				for work_node in worklist:
					for work_input in work_node.in_edges:
						if work_input.tail not in worklist:
							inputlist.append((work_input.width, work_input.tail))

				for edge in bottom.in_edges:
					edge.set_width(bottom_width)
				worklist.remove(bottom)
				edgelist = []
				edgelist.extend(bottom.in_edges)
				while(len(worklist)):
					current_edge = edgelist.pop(0)
					current_node = worklist.pop(0)
					if current_node.type_string in ['c', 'in', 'bitext']:
						current_edge.tail_pos = None
					else:
						current_edge.tail_pos = 'out'
					current_edge.set_width(bottom_width)
					current_edge.tail = current_node
					edgelist.extend(current_edge.tail.in_edges)
				while(len(inputlist)):
					current_edge = edgelist.pop(0)
					current_width, current_input = inputlist.pop(0)

					if current_input.type_string in ['c', 'in', 'bitext']:
						current_edge.tail_pos = None
					else:
						current_edge.tail_pos = 'out'
					current_edge.set_width(current_width)
					current_edge.tail = current_input
				assert(len(worklist) == 0)
				assert(len(edgelist) == 0)
				assert(len(inputlist) == 0)
		else:
			node.visited = True


def visit(node, worklist, bottom, opts):

	if not node.visited:
		#print('adding node ' + node.ID)
		node.visited = True
		worklist.append(node)
		to_visit = None
		other_outputs = False
		for pred in node.in_edges:
			node2 = pred.tail
			if node2.type_string in opts:
				#print(node.ID +' calling visit to input edge')
				bottom = visit(node2, worklist, bottom, opts)


		for succ in node.out_edges:
			node2 = succ.head
			if node2.type_string in opts:
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
			bottom = visit(bottom, worklist, bottom, opts)
		elif (node != bottom):
			worklist.remove(node)
	
	#else:
		#print(node.ID +'already visited')
	return bottom



