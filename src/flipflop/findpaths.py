from collections import deque
import copy

def run(graph):
    inputnodes = []
    outputnodes = []
    print("Graph contains nodes:", len(graph.nodes.items()))
    for ID,node in graph.nodes.items():
        if node.type_string in ['in', 'validin', 'pidin']:
            inputnodes.append(node)
        if node.type_string in ['out']: # TODO there might be other types of out nodes
            outputnodes.append(node)

    paths = 0
    for node in inputnodes:
        paths += findpath(node)
        print(str(node), paths)
        # break

    print('found', paths)

    # pathdict = {} # ID -> [[path1], [path2]]
    # while outputnodes:
    #     worklist = deque([outputnodes.pop()])
    # # worklist = deque(graph.nodes.values())
    #     while len(worklist) > 0:
    #         node = worklist.pop()
    #         print(str(node), len(worklist), len(pathdict))
    #         paths = []
    #         if len(node.out_edges) == 0:
    #             paths = [[node.ID]]
    #         else:
    #             for outedge in node.out_edges:
    #                 for path in pathdict[outedge.head.ID]:
    #                     paths.append([node.ID] + path)
            
    #         pathdict[node.ID] = paths
    #         for out_edge in node.out_edges:
    #             if solved(out_edge.head, pathdict):
    #                 pathdict.pop(out_edge.head.ID)
    #         for in_edge in node.in_edges:
    #             worklist.append(in_edge.tail)

    # for inp in inputnodes:
    #     print(pathdict[inp.ID])

allpaths = []
pathdict = {}

def findpath(node):
    if node.type_string == 'out':
        return 1
    if node.ID in pathdict:
        return pathdict[node.ID]
    sumpaths = 0
    for outedge in node.out_edges:
        sumpaths += findpath(outedge.head)
    pathdict[node.ID] = sumpaths
    print(sumpaths)
    return sumpaths

def solved(node, pdict):
    for in_edge in node.in_edges:
        if not in_edge.tail in pdict:
            return False
    return True

    # paths = []
    # for node in inputnodes:
    #     paths += findpaths(node)
    # print(len(paths))
    # print(paths)
    # for path in paths:
    #     for node in path:
    #         print(str(node.type_string) + ', '),
    #     print("")


# recursive algorithm breaks due to space complexity
def findpaths(node):
    if node.ID in pathdict:
        return pathdict[node.ID]
    # print(len(pathdict))
    if node.type_string in ['out', 'validout', 'pidout']:
        return [[node.ID]]
    paths = []
    for edge in node.out_edges:
        outpaths = findpaths(edge.head) # [[b, a], [c, a]]
        for path in outpaths:           # [b, a]
            paths.append([node.ID] + path) # path += [x, b, a]
                                        # path = [[x, b, a], [x, c, a]]
    # print(node)
    # print(paths[0][0].__str__(), paths[0][-1].__str__())    
    # pathdict[node.ID] = paths
    return paths