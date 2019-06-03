import heapq
import copy
from util.Node_Pair import Node_Pair
from util.Node import Node
from util.Graph import Graph
import sys
filenumber = 0

def run(graph, target_delay, mergefactor):

    # set up values for comparing potential merges
    Node_Pair.nodefactor = mergefactor
    Node_Pair.edgefactor = 1-mergefactor


    # check that target_delay is large enough 
    for node in graph.nodes.values():
        x = int(node.info["operator_delay"]) 
        if x > target_delay:
            print("DELAY TOO LOW, INCREASING TO: {}".format(x))
            target_delay = x

    # merge nodes in graph copy
    # then apply flipflops to original
    original = graph
    graph = original.create_copy()

    # find nodes which have at 
    # least one edge between them
    node_pairs = []
    edge_max = 0
    for edge in graph.edges:
        n = Node_Pair(edge.tail, edge.head)
        if len(n.edges) != 0:
            node_pairs.append(n)
        if edge.width > edge_max:
            edge_max = edge.width
    
    # values needed for comparing Node_Pairs
    Node_Pair.nodemax = target_delay
    Node_Pair.edgemax = edge_max

    # debuging
    printgraph(graph)


    while node_pairs:
        node_pairs.sort()
        node_pair = node_pairs.pop()
        print("node_pairs:", len(node_pairs), str(node_pair.mergevalue()))
        if node_pair.can_merge(target_delay):
            merge(graph, node_pair, node_pairs)
    

    # for edge in graph.edges:
    #     ref = edge.reference_edge
    #     if not ref:
    #         print("edge has no reference!!:", edge)
    #         exit(-1)
    #     original.insert_FF(ref)

    # for node in graph.nodes.values():
    #     if 0 == len(node.out_edges) == len(node.in_edges):
    #         graph.remove_node(node)

    outputnodes = []
    inputnodes = []
    for node in graph.nodes.values():
        if not node.out_edges:
            outputnodes.append(node)
        if not node.in_edges:
            inputnodes.append(node)

    # print("RECURSION LIMIT CHANGED TO ", len(graph.nodes))
    # sys.setrecursionlimit(len(graph.nodes))

    printgraph(graph)

    for node in outputnodes:
        print("output")
        set_pipeline_stage(node, 0)
    
    max_pl = 0
    for node in inputnodes:
        val = node.info["pl_stage"]
        if val > max_pl:
            max_pl = val
    for node in inputnodes:
        node.info["pl_stage"] = max_pl
        print(str(node), node.info["pl_stage"])
    
    # sets FF based on pipeline stage
    for edge in graph.edges[:]:
        print(edge)
        diff = edge.tail.info["pl_stage"] - edge.head.info["pl_stage"]
        ref = edge.reference_edge
        # edge.set_width(diff)
        while diff > 0:
            print("insert ff", diff)
            FF = original.insert_FF(ref)
            ref = FF.out_edges[0]
            diff -= 1    



    print("DONE WITH NODEMERGING, NODE COUNT:", len(graph.nodes))
    printgraph(graph)


def set_pipeline_stage(node, pl_stage):
    # print(pl_stage, node)
    if "pl_stage" in node.info:
        if node.info["pl_stage"] >= pl_stage:
            # node has been solved and does not need to be recalculated
            return
    # pl_stage has increased, parents need recalculating
    node.info["pl_stage"] = pl_stage
    if not node.in_edges:
        return
    for edge in node.in_edges:
        set_pipeline_stage(edge.tail, pl_stage+1)



def merge(graph, nodepair, nodepair_list):
    a = nodepair.node_a
    b = nodepair.node_b
    # print('merging', str(a), str(b), len(nodepair.edges), nodepair.edge_weight(), nodepair.combined_size())
    nodes = graph.nodes.values()
    
    # TODO improve execution time by removing 
    # node_pairs from worklist when merging
    if a not in nodes:
        # print("a does not exist, returning")
        return
    if b not in nodes:
        # print("b does not exist, returning")
        return

    if not a.in_edges and not b.out_edges:
        # do not merge input and output nodes
        return
    info = {
        'label': 'merge'+a.ID+b.ID,
        'operator_delay': nodepair.combined_size(),
    }
    type_string = 'mergednode'
    node = Node(type_string, ID=None, **info)

    out_nodes = []
    in_nodes = []

    for edge in a.in_edges[:]:
        if edge.tail is b:
            continue
        new_edge = graph.create_edge(edge.tail, node, edge.width, edge.tail_pos, None, None)
        new_edge.reference_edge = edge.reference_edge
        if edge.tail not in in_nodes:
            in_nodes.append(edge.tail)
        graph.remove_edge(edge)
    for edge in b.in_edges[:]:
        if edge.tail is a:
            continue
        new_edge = graph.create_edge(edge.tail, node, edge.width, edge.tail_pos, None, None)
        new_edge.reference_edge = edge.reference_edge
        if edge.tail not in in_nodes:
            in_nodes.append(edge.tail)
        graph.remove_edge(edge)

    for edge in a.out_edges[:]:
        if edge.head is b:
            continue
        new_edge = graph.create_edge(node, edge.head, edge.width, None, edge.head_pos, None)
        new_edge.reference_edge = edge.reference_edge
        if edge.head not in out_nodes:
            out_nodes.append(edge.head)
        graph.remove_edge(edge)

    for edge in b.out_edges[:]:
        if edge.head == a:
            continue
        new_edge = graph.create_edge(node, edge.head, edge.width, None, edge.head_pos, None)
        new_edge.reference_edge = edge.reference_edge
        if edge.head not in out_nodes:
            out_nodes.append(edge.head)
        graph.remove_edge(edge)
    
    for p in nodepair_list[:]:
        if p.node_a in [a, b] or p.node_b in [a, b]:
            nodepair_list.remove(p)

    for inp in in_nodes:
        if inp != node:
            nodepair_list.append(Node_Pair(inp, node))
    
    for out in out_nodes:
        if out != node:
            nodepair_list.append(Node_Pair(out, node))
    

    graph.remove_node(a)
    graph.remove_node(b)

    graph.nodes[node.ID] = node


def printgraph(graph):
    global filenumber
    if filenumber < 20:
        graph.write_to_file(open('filename'+str(filenumber), 'w'))
        filenumber += 1
    else:
        print("cannot create more files!")

exitcount = {}
def countToExit(node):
    if not node.out_edges:
        return 0
    if node in exitcount:
        return exitcount[node]
    count = 0
    for edge in node.out_edges:
        c = countToExit(edge.head)
        if c > count:
            count = c
    exitcount[node] = count+1
    return count+1
