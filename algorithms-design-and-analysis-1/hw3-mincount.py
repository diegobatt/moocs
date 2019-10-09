import copy
import ipdb
import random
from math import inf, log2

def karger_min_cuts(g): # n : vertices, m: edges

    graph = copy.deepcopy(g)
    n = len(graph)

    while n > 2:

        edge_start = random.choice(list(graph.keys()))
        edge_end = random.choice(graph[edge_start])
        new_vertex = (edge_start, edge_end)

        for k, v in graph.items():
            conns = v.copy()
            j = 0
            for i, vertex in enumerate(conns):
                if vertex in new_vertex:
                    if k in new_vertex:
                        v.pop(j)
                    else:
                        v[i] = new_vertex
                        j += 1
                else:
                    j += 1

        graph[new_vertex] = graph[edge_start] + graph[edge_end]
        graph.pop(edge_start)
        graph.pop(edge_end)

        n -= 1

    groups = list(graph.keys())
    assert len(graph[groups[0]]) == len(graph[groups[1]])

    return len(graph[groups[0]])

if __name__ == '__main__':
    import csv
    import sys

    try:
        filepath = sys.argv[1]
        graph = dict()
        with open(filepath) as f: 
            csv_reader = csv.reader(f, delimiter='\t')
            for row in csv_reader:
                graph[row[0]] = row[1:-1] # Last char is blank for some reason
    except:
        graph = {
            1: [2, 2, 3, 6],
            2: [1, 1, 4, 3, 7],
            3: [4, 1, 2, 5, 6],
            4: [2, 3, 5, 7],
            5: [3, 4, 6, 8],
            6: [1, 5, 3],
            7: [4, 2],
            8: [5]
        }

    n = len(graph)
    N = int(n * log2(n))
    min_cuts = inf

    for i in range(N):
        new_cuts = karger_min_cuts(graph)
        min_cuts = new_cuts if new_cuts < min_cuts else min_cuts

    print(f"Minimum cuts: {min_cuts}")
