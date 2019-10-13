import sys

import progressbar

VFROM, VTO, VEXPLORED = 0, 1, 2

def dfs_recursive(graph, order=[], vertex=0, backwards=True):

    vertices = VFROM if backwards else VTO
    if graph[vertex][VEXPLORED] == True:
        return set()
    graph[vertex][VEXPLORED] = True
    conns = {vertex}

    for new_vertex in graph[vertex][vertices]:
        if graph[new_vertex][VEXPLORED] == False:
            new_conns = dfs_recursive(graph, order, new_vertex, backwards)
            conns.update(new_conns)

    order.append(vertex)
    
    return conns

def dfs_stack(graph, order=[], vertex=1, backwards=True):

    vertices = VFROM if backwards else VTO
    stack = [vertex]
    is_final = [False]
    conns = set()

    while stack:
    
        if is_final[-1]:
            v = stack.pop()
            is_final.pop()
            order.append(v)
            continue

        v = stack[-1]
        if graph[v][VEXPLORED]:
            stack.pop()
            is_final.pop()
            continue

        is_final[-1] = True
        graph[v][VEXPLORED] = True
        conns.add(v)

        for new_v in graph[v][vertices]:
            if not graph[new_v][VEXPLORED]:
                stack.append(new_v)
                is_final.append(False)
              
    return conns

def set_unexplored(graph):
    for _, v in graph.items():
        v[VEXPLORED] = False

def get_topological_order(graph, backwards=True):
    set_unexplored(graph)
    order = []

    for k, v in progressbar.progressbar(graph.items()):
        if v[VEXPLORED] == False:
            # dfs_recursive(graph, order, k, backwards)
            dfs_stack(graph, order, k, backwards)

    return order

def get_scc(graph):
    sccs = []
    print("Fist DFS loop")
    order = get_topological_order(graph, backwards=True)
    set_unexplored(graph)

    print("Second DFS loop")
    for i in progressbar.progressbar(order[::-1]):
        if graph[i][VEXPLORED] == False:
            # sccs.append(dfs_recursive(graph, [], i, False))
            sccs.append(dfs_stack(graph, [], i, False))
    
    return sccs

if __name__ == '__main__':
    import csv
    import sys

    try:
        filepath = sys.argv[1]
        graph = {}
        with open(filepath) as f:
            csv_reader = csv.reader(f, delimiter=' ')
            for row in csv_reader:
                from_, to_ = int(row[0]), int(row[1])
                if from_ in graph:
                    graph[from_][1].add(to_)
                else:
                    graph[from_] = [set(), set([to_]), False]
                if to_ in graph:
                    graph[to_][0].add(from_)
                else:
                    graph[to_] = [set([from_]), set(), False]
    except:
        graph = {
            0: [{2, 0}, {1, 0}, False],
            1: [{0}, {2}, False],
            2: [{1}, {0, 3}, False],
            3: [{2, 5}, {4}, False],
            4: [{3, 7}, {5}, False],
            5: [{4}, {3, 6}, False],
            6: [{5}, {7}, False],
            7: [{6, 9}, {8, 4}, False],
            8: [{7}, {9}, False],
            9: [{8}, {7}, False]
        }

    sccs = get_scc(graph)
    size_sccs = [len(scc) for scc in sccs]
    size_sccs.sort()
    print(size_sccs[-5:])

