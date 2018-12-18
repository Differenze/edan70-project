
extra_output_bits = {
	'opadd'		:	1,
	'opsub'		:	1, # subtraction result is 0 padded
	'opor'		:	0,
	'opand'		:	0,
	'opxor'		:	0,
}

def run(graph):
	worklist = list(graph.nodes.values())
	num = 0

	# file = open('tempfile'+str(num)+'.dot', 'w')
	# graph.write_to_file(file)
	# file.close()
	# num += 1

	while worklist:
		node = worklist.pop()
		if node.type_string in extra_output_bits.keys():
			max_input = 0
			for edge in node.input_edges():
				if edge.width > max_input:
					max_input = edge.width
			max_output = 0
			for edge in node.output_edges():
				if edge.width > max_output:
					max_output = edge.width

			for edge in node.input_edges():
				if edge.width > max_output:
					edge.set_width(max_output)
					worklist.append(edge.tail)
			for edge in node.output_edges():
				if edge.width > max_input+extra_output_bits[node.type_string]:
					edge.set_width(max_input+extra_output_bits[node.type_string])
					worklist.append(edge.head)

			# print(node)
			# file = open('tempfile'+str(num)+'.dot', 'w')
			# graph.write_to_file(file)
			# file.close()
			# num += 1