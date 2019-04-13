def run(graph):
    for node in graph.nodes.values():
        print(node.dot_string(), node.obj_dict['attributes']['label'])