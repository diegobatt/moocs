import heapq
from collections import namedtuple
from math import inf


E = namedtuple('Edge', ['vertex', 'lenght'])

def dijkstra(graph, source=0):

    n = len(graph)
    spls = [inf] * n  # Shortest path lenghts
    seen = [False] * n
    spls[source] = 0
    reached = []
    heapq.heappush(reached, (spls[source], source))

    while len(reached) != 0:
        spl, v = heapq.heappop(reached)
        seen[v] = True
        for e in graph[v]:
            if not seen[e.vertex]:
                score = spl + e.lenght
                if spls[e.vertex] > score:
                    spls[e.vertex] = score
                    heapq.heappush(
                        reached, (score, e.vertex))
    
    return spls
            
            

if __name__ == '__main__':
    import csv
    import sys

    try:
        filepath = sys.argv[1]
        graph = []
        with open(filepath) as f: 
            csv_reader = csv.reader(f, delimiter='\t')
            # for row in csv_reader:
            #     graph[row[0]] = row[1:-1] # Last char is blank for some reason
    except:
        graph = [
            [E(1, 1), E(2, 3)],
            [E(2, 1)],
            [E(3, 1), E(4, 3)],
            [E(4, 4)],
            []
        ]
    
    aux = dijkstra(graph, source=0)
    print(aux)
    import ipdb; ipdb.set_trace()