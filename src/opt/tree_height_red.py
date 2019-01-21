# finds subgraphs of similar operations which are normally commutitive, evaluates their sizes to be equal and then balances the graph. 
# proved difficult as operations with different sized inputs or outputs are not commutitive due to overflow. 
# More information about overflow and how the sizes of operations is determined could improve this optimization.


def run(graph, opt):
	opts = None
	if (opt == 'add'):
		opts = ['opadd', 'opsub']
	elif (opt == 'and'):
		opts = ['opand']
	elif (opt == 'or' ):
		opts = ['opor']

	for ID,node in graph.nodes.items():
		# A way of limiting what nodes the program will run on. max once per node and only if its relevant to the optimization
		if not node.visited and node.type_string in opts:
			worklist = []
			# bottom is the base of the 'tree'
			bottom = node

			bottom = visit(node, worklist, bottom, opts)
			#greatest width of the edges out of the bottom node.
			bottom_width = 0
			for edge in bottom.out_edges:
				if edge.width > bottom_width:
					bottom_width = edge.width
			#if the width for a node is not the same as the bottom width they are removed from the worklist to prevent faulty outputs due to overflows.
			for work_node in list(worklist):
				if work_node != bottom and work_node.out_edges[0].width != bottom_width:
					worklist.remove(work_node)
					work_node.visited = False
			# A subgraph has been found and balancing can begin.
			# implemented by creating a list of all iputs into the subgraph, inputlist
			# and then creating a balanced tree with the very same inputs.

			if len(worklist)>2:
				inputlist = []
				#fills inputlist
				for work_node in worklist:
					for work_input in work_node.in_edges:
						if work_input.tail not in worklist:
							inputlist.append((work_input.width, work_input.tail))
				for edge in bottom.in_edges:
					edge.set_width(bottom_width)
				worklist.remove(bottom)
				# This edgelist serves multiple purposes. It is the list of all edges currently going into the subgraph as its being built.
				# It will be appended for each node added to the graph. When there are no more nodes to add it will instead be filled with the inputs.
				edgelist = []
				edgelist.extend(bottom.in_edges)

				# builds the subtree
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
				# fills the remaining edges with the saved inputs
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


# Recursively traverses the graph to fill the worklist with nodes of the subgraph as well as finds the bottom node.
def visit(node, worklist, bottom, opts):

	if not node.visited:
		node.visited = True
		worklist.append(node)
		to_visit = None
		other_outputs = False
		for pred in node.in_edges:
			node2 = pred.tail
			if node2.type_string in opts:
				bottom = visit(node2, worklist, bottom, opts)


		for succ in node.out_edges:
			node2 = succ.head
			if node2.type_string in opts:
				if to_visit == None:
					to_visit = node2
				else:
					to_visit = None
					break
			else:
				other_outputs = True

		if to_visit != None and not other_outputs:
			bottom = to_visit
			bottom = visit(bottom, worklist, bottom, opts)
		elif (node != bottom):
			worklist.remove(node)

	return bottom



