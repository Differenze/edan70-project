

class Node_Pair:
    edgefactor = 0.5
    nodefactor = 1-edgefactor
    # set these!
    edgemax = 0
    nodemax = 0

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
        return int(self.node_a.info['operator_delay'])+int(self.node_b.info['operator_delay'])

    def can_merge(self, target_delay):
        if target_delay < self.combined_size():
            return False
        print('bfs1')
        bfs_value1 = self.bfs_check_path_to_b() # true if there is a path from a to b
        print('bfs2')
        bfs_value2 = self.bfs_check_path_to_a() # true if there is a path from b to a
        return (not bfs_value1) and (not bfs_value2) #TODO fix this chaos

    # returns true if there are paths between a and b which contain other nodes 
    def bfs_check_path_to_b(self):
        worklist = []
        for edge in self.node_a.out_edges:
            if edge.head is self.node_b:
                continue
            worklist.append(edge.head)
        while worklist:
            # avoid getting into infinite loops
            if len(worklist) > 20: # TODO set this to the highest possible value 40 works
                return True
            current = worklist.pop()
            for edge in current.out_edges:
                if edge.head is self.node_b:
                    return True
                worklist.append(edge.head)        
        return False

    def bfs_check_path_to_a(self):
        worklist = []
        for edge in self.node_b.out_edges:
            if edge.head is self.node_a:
                continue
            worklist.append(edge.head)
        while worklist:
            # avoid getting into infinite loops
            if len(worklist) > 20: # TODO set this to the highest possible value 40 works
                return True
            current = worklist.pop()
            for edge in current.out_edges:
                if edge.head is self.node_a:
                    print("thing", str(edge.tail), str(edge.head))
                    return True
                worklist.append(edge.head)        
        return False

    # < operator used by sort
    # used to determine which nodes to merge
    def __lt__(self, other):
        # return self.edge_weight() < other.edge_weight()
        return self.mergevalue() < other.mergevalue()

    # greater means higher chance to be merged
    def mergevalue(self):
        # larger edgeweight means more expensive to not merge
        norm_edge = self.edge_weight()/float(Node_Pair.edgemax)
        # assumption, merging two nodes with large combined size is good???
        norm_node = self.combined_size()/float(Node_Pair.nodemax)
        return  norm_edge*Node_Pair.edgefactor + norm_node*Node_Pair.nodefactor
