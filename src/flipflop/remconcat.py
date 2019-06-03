def run(graph):
    numremoved = 0
    for node in graph.nodes.values():
        if node.type_string == 'bitconcat':
            base = node.in_edges[0]
            allsame = True
            for edge in node.in_edges:
                if edge.tail != base.tail:
                    allsame = False
            
            if allsame:
                for out_edge in node.out_edges:
                    tail = base.tail
                    tail_pos = base.tail_pos
                    head = out_edge.head
                    head_pos = out_edge.head_pos
                    width = base.width
                    graph.create_edge(tail, head, width, tail_pos, head_pos)
                print(node)
                graph.remove_node(node)
                numremoved += 1
    
    print('removed '+str(numremoved)+' bitconcats')