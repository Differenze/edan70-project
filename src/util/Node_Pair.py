

class Node_Pair:

    def __init__(self, node_a, node_b):
        self.node_a = node_a
        self.node_b = node_b
        self.edges = []
        for edge in node_a.out_edges:
            if edge.head == node_b:
                self.edges.append(edge)

    def edge_weight(self):
        s = 0
        for edge in self.edges:
            s += edge.width
        return s

    def combined_size(self):
        return node_a.info['operator_delay']+node_b.info['operator_delay']

    def __lt__(self, other):
        return self.edge_weight() < other.edge_weight()