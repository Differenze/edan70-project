def run(graph):
    FF_edges = [] # TODO remove
    for ID,node in graph.nodes.items():
        if node.type_string in ['ff', 'pidff', 'validff']:
            for in_edge in node.in_edges:
                for out_edge in node.out_edges:
                    tail = in_edge.tail
                    tail_pos = in_edge.tail_pos
                    head = out_edge.head
                    head_pos = out_edge.head_pos
                    width = in_edge.width
                    e = graph.create_edge(tail, head, width, tail_pos, head_pos)
                    FF_edges.append(e) # TODO remove
            graph.remove_node(node)
            
            
    
    # TODO remove, used for debugging graph.insert_FF
    # for node in graph.nodes.values():
    #     if node.type_string == 'c':
    #         for edge in node.out_edges[:]:
    #             print(edge)
    #             graph.insert_FF(edge)