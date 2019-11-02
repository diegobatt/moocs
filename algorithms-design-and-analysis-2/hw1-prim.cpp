#include <iostream>
#include <fstream>
#include <algorithm>
#include <vector>
#include <string>

using namespace std;

struct Edge {
    int to;
    int weight;
};
bool edgecmp(Edge left, Edge right) { return left.weight > right.weight; };

struct Node {
    size_t id;
    vector<Edge> edges;
};

struct Graph {
    size_t n;
    size_t m;
    vector<Node> nodes;
};

Graph read_file(const char * filename) {

    size_t from, to;
    int weight;
    Edge edge;
    Graph graph;
    ifstream fin;

    fin.open(filename);

    if (!fin.is_open()) {
        cout << "Could not open file: " << filename << endl;
        return graph;
    };

    fin >> graph.n >> graph.m;
    cout << "We have " << graph.n << " nodes and " << graph.m << " edges" << endl;

    graph.nodes.resize(graph.n);

    while(fin >> from >> to >> weight) {
        edge.weight = weight;
        edge.to = to - 1;
        graph.nodes[from - 1].edges.push_back(edge);
        edge.to = from - 1;
        graph.nodes[to - 1].edges.push_back(edge);
    };

    fin.close();

    return graph;
};

int mst(Graph graph) {

    size_t i, count = 1;
    int total = 0;
    Node aux_node = graph.nodes[0];
    Edge aux_edge;
    vector<Edge> heap;
    bool explored[graph.n] = {false};
    
    for(i=0; i<aux_node.edges.size(); i++){
        heap.push_back(aux_node.edges[i]);
        push_heap(heap.begin(), heap.end(), edgecmp);
    };
    explored[0] = true;

    while(!heap.empty()) {
        aux_edge = heap.front();
        pop_heap(heap.begin(), heap.end(), edgecmp); 
        heap.pop_back(); 
        if (explored[aux_edge.to] == false) {
            explored[aux_edge.to] = true;
            total += aux_edge.weight;
            aux_node = graph.nodes[aux_edge.to];
            for(i=0; i<aux_node.edges.size(); i++){
                heap.push_back(aux_node.edges[i]);
                push_heap(heap.begin(), heap.end(), edgecmp);
            };
        };
    };
    return total;
};

int main(int argc, char** argv) {

    Graph graph;
    size_t i, j;
    int total;

    if(argc!=2) {
        cout << "Please indicate a graph file" << endl;
        return 1;
    };

    graph = read_file(argv[1]);

    total = mst(graph);
    cout << "Minimum cost: " << total << endl;

    return 0;
};