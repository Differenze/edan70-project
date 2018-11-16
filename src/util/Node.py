

class Node:
	dot_string = ''
	graph_id = ''
	type_string = ''
	ID = -1

	
	def __init__(self, dot_string=None):
		if dot_string:
			self.parse(dot_string)


	# Parse line from dot file
	def parse(self, dot_string):
		dot_string = dot_string.replace('\n', '')
		self.dot_string = dot_string
		self.graph_id = dot_string.split()[0]
		self.type_string = self.graph_id.split('_')[0]
		self.ID = self.graph_id.split('_')[-1]


	# Output this node as dot format
	def dot_output(self):
		return dot_string + '\n'