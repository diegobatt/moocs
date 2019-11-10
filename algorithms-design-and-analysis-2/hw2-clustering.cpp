#include <vector>
#include <iostream>
#include <fstream>
#include <algorithm>
#include "union-find.hpp"

using namespace std;

struct Edge {
    int from;
    int to;
    int value;

    bool operator<(const Edge& other) const {
        return value < other.value;
    };
};

struct Graph {
    vector<Edge> edges;
    size_t n;
};

Graph read_file(const char * filename) {

    Edge aux_edge;
    Graph graph;
    int i, aux_from, aux_to;
    ifstream fin;

    fin.open(filename);

    if (!fin.is_open()) {
        cout << "Could not open file: " << filename << endl;
        return graph;
    };

    fin >> graph.n;
    cout << "We have " << graph.n << " nodes" << endl;

    while(fin >> aux_from >> aux_to >> aux_edge.value) {
        aux_edge.from = aux_from - 1;
        aux_edge.to = aux_to - 1;
        graph.edges.push_back(aux_edge);
    };

    fin.close();

    return graph;
}

int max_space_clustering(vector<Edge> edges, int nodes, int K) {

    size_t N = edges.size();
    size_t i = 0;
    UF clusters(nodes);

    sort(edges.begin(), edges.end());
    while (clusters.size > K) {
        clusters.merge(edges[i].from, edges[i].to);
        i++;
        if (i > N) { break; }
    }
    for (i; i < N; i++) {
        if (clusters.find(edges[i].from) != clusters.find(edges[i].to)) {
            return edges[i].value;
        }
    }

    return 0;
}

int main(int argc, char** argv) {

    Graph graph;

    if(argc!=2) {
        cout << "Please indicate a graph file" << endl;
        return 1;
    };

    graph = read_file(argv[1]);

    cout << "Max spacing is: " << max_space_clustering(graph.edges, graph.n, 4) << endl;
    
    return 0;
}