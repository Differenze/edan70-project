def run(graph):
    for ID,node in graph.nodes.items():
        if node.type_string in ['ff', 'pidff', 'validff']:
            node.in_edges
            node.out_edges
            for in_edge in node.in_edges:
                for out_edge in node.out_edges:
                    tail = in_edge.tail
                    tail_pos = in_edge.tail_pos
                    head = out_edge.head
                    head_pos = out_edge.head_pos
                    width = in_edge.width
                    graph.create_edge(tail, head, width, tail_pos, head_pos)
            graph.remove_node(node)

            # tail = node.in_edges[0].tail
            # tail_pos = node.in_edges[0].tail_pos
            # head = node.out_edges[0].head
            # head_pos = node.out_edges[0].head_pos
            # width = node.out_edges[0].width