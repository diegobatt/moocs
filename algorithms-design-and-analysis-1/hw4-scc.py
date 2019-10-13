import progressbar
import resource
import sys

resource.setrlimit(resource.RLIMIT_STACK, (resource.RLIM_INFINITY, resource.RLIM_INFINITY))
sys.setrecursionlimit(2 ** 17)
VFROM, VTO, VEXPLORED = 0, 1, 2

def dfs(graph, order=[], current=[], vertex=0, backwards=True):

    vertices = VFROM if backwards else VTO
    graph[vertex][VEXPLORED] = True
    conns = {vertex}

    for new_vertex in graph[vertex][vertices]:
        if graph[new_vertex][VEXPLORED] == False:
            new_conns = dfs(graph, order, current, new_vertex, backwards)
            conns.update(new_conns)

    if current:
        order.append(vertex)
        current[0] -= 1
    
    return conns

def dfs_stack(graph, order=[], vertex=0, backwards=True):

    label = len(graph)
    vertices = VFROM if backwards else VTO
    stack = [vertex]
    conns = set()

    import ipdb; ipdb.set_trace()
    while stack:
        v = stack.pop()
        if graph[v][VEXPLORED] == False:
            graph[v][VEXPLORED] = True
            conns.add(v)
            new_vs = graph[v][vertices]
            if new_vs:
                stack.extend(graph[v][vertices])
            else:
                order.append(v)
                label -= 1
    
    return conns

def set_unexplored(graph):
    for _, v in graph.items():
        v[VEXPLORED] = False

def get_topological_order(graph, backwards=True):
    set_unexplored(graph)
    current = [len(graph) - 1]
    order = []

    for k, v in graph.items():
        if v[VEXPLORED] == False:
            # dfs(graph, order, current, k, backwards) # Pointer to current
            dfs_stack(graph, order, k, backwards) # Pointer to current

    return order

def get_scc(graph):
    sccs = []
    order = get_topological_order(graph, backwards=True)
    set_unexplored(graph)

    for i in progressbar.ProgressBar(order[::-1]):
        if graph[i][VEXPLORED] == False:
            sccs.append(dfs(graph, [], [], i, False)) # Pointer to current
    
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

    import ipdb; ipdb.set_trace()
    print(get_topological_order(graph, backwards=False))
    # print(get_topological_order(graph, backwards=True))
    import ipdb; ipdb.set_trace()
    # print(get_scc(graph))
