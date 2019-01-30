# --bitwidth
# analyses the bit width necessary for each operation


# keys are a list of nodes which can be resized
# values is how many carry bits should be considered
extra_output_bits = {
	'opadd'		:	1,
	'opsub'		:	1, # subtraction result is 0 padded
	'opor'		:	0,
	'opand'		:	0,
	'opxor'		:	0,
}

def run(graph):
	worklist = list(graph.nodes.values())

	while worklist:
		node = worklist.pop()
		if node.type_string in extra_output_bits.keys():
			max_input = 0 # max amount of bits in input
			for edge in node.input_edges():
				if edge.width > max_input:
					max_input = edge.width
			max_output = 0 # max amount of bits in output
			for edge in node.output_edges():
				if edge.width > max_output:
					max_output = edge.width

			# update input edges based on max_output
			for edge in node.input_edges():
				if edge.width > max_output:
					edge.set_width(max_output)
					worklist.append(edge.tail)
			
			# update output edges based on max_input
			for edge in node.output_edges():
				if edge.width > max_input+extra_output_bits[node.type_string]:
					edge.set_width(max_input+extra_output_bits[node.type_string])
					worklist.append(edge.head)
