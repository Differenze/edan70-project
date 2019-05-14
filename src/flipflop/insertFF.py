import operator


def run(graph):
	path = getLongestPath(graph)[1]
	insertFFGreedy(graph, path, 15)
	
# optpaths is a list with the opt path given that a FF is inserted after the node
def opt(index, path, size, optpaths):
	sizeLeft = size-path[index].info['dealy']
	if sizeLeft<0:
		print("Size too low!")
		print(path[index].label)
		print(path[index].info['delay'])
		print(size)
		return
	min = 0
	originalIndex = index
	# includes one negative sizeLeft because flipFlops are inserted after the node
	while sizeLeft:
		index -= 1
		prev = path[index]
		sizeLeft -= path[index].info['dealy']
		indexMin = opt(index, path, size)
		if indexMin > max:
			min = indexMin
			copyPath =  optpaths[index][:]
			optpaths[originalIndex] = copyPath.append(path[originalIndex])
	min += path[originalIndex].info['width']
	return min





# def insertFFPro(graph, path, size):
# 	# list of each nodes options. ordered by the nodex index
# 	#  [[option1, opt2, opt3],[]]
# 	optList = []
# 	for i, node in enumerate(path):
# 		for j in range(j,-1,-1):


def insertFFGreedy(graph, path, size):
	sizeLeft = size
	prev = None
	for node in path:
		if int(node.info['delay']) > size:
			print("Size too low!")
			print(node.label)
			print(node.info['delay'])
			print(size)
			
			break
		if (sizeLeft >= int(node.info['delay'])):
			sizeLeft -= int(node.info['delay'])
		else:
			node.insertFF(graph)
			sizeLeft = size
		prev = node


# finds the longest path from the in node
def getLongestPath(graph):

	for ID,node in graph.nodes.items():
		if node.type_string == 'in' and node.label[:5] == 'sourc':
			# print('Found!')
			tup = getLongest(node)
			# print(tup[0])
			# print(len(map))
			# sorted_list = sorted(map.items(), key=operator.itemgetter(1), reverse=True)
			# print('--------------')
			# for tupl in sorted_list:
			# 	if tupl[0] not in tup[1]:
			# 		print(tupl[1][0])	
			return tup	

# fills map with (node,(length to out, path to out)) and returns (length to out, path to out)
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
			path = tup[1][:]
			path.append(node)
	return (max, path)

# paths = []
# tempPaths = {}

# def run(graph):
# 	outNodes = []
# 	for ID,node in graph.nodes.items():
#  		if node.type_string == 'out':
#  			outNodes.append(node)

#  	while outNodes:
#  		print(len(outNodes))

#  		worklist = [outNodes.pop()]
#  		while(worklist):
# 	 		node = worklist.pop()
# 	 		toAdd = []
# 	 		for edge in node.out_edges:
# 	 			succ = edge.head
# 	 			if succ in tempPaths:
# 	 				succPaths = tempPaths[succ]
# 	 				for path in succPaths:
# 	 					t = path[:]
# 	 					t.append(node)
# 	 					toAdd.append(t)
# 	 		if not toAdd:
# 	 			toAdd = [[node]]
# 	 		tempPaths[node] = toAdd
	 		

# 	 		if node.type_string == 'in':
# 	 			paths.append(toAdd)
# 	 			# print(len(paths))
# 	 		else:
# 		 		for edge in node.in_edges:
# 		 			pred = edge.tail
# 		 			worklist.append(pred)
# 	print(len(paths))