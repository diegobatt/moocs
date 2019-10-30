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
bool edgecmp(Edge left, Edge right) { return left.weight < right.weight; }

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

    size_t i;
    Node aux_node = graph.nodes[0];
    vector<Edge> heap;
    bool explored[graph.n];
    
    for(i=0; i<aux_node.edges.size(); i++){
        heap.push_back(aux_node.edges[i]);
        push_heap(heap.begin(), heap.end());
    };

    while(!heap.empty()) {
        
    };
};

int main(int argc, char** argv) {

    Graph graph;
    size_t i, j;

    if(argc!=2) {
        cout << "Please indicate a graph file" << endl;
        return 1;
    };

    graph = read_file(argv[1]);

    for(i=0; i<graph.n; i++){
        for(j=0; j<graph.nodes[i].edges.size(); j++){
            cout << graph.nodes[i].edges[j].to << ", ";
        };
        cout << "\n";
    };

    return 0;
};