#include <vector>
#include <iostream>
#include <fstream>
#include <algorithm>
#include <math.h>
#include "union-find.hpp"

using namespace std;

struct Graph {
    vector<int> values;
    size_t n;
    size_t bits;
};

Graph read_file(const char * filename) {

    size_t i;
    int bit;
    int value;
    Graph graph;
    ifstream fin;

    fin.open(filename);

    if (!fin.is_open()) {
        cout << "Could not open file: " << filename << endl;
        return graph;
    };

    fin >> graph.n >> graph.bits;
    cout << "We have " << graph.n << " nodes, expresed with " << graph.bits << " bits." << endl;

    while (true) {
        value = 0;
        for (i = 0; i < graph.bits; i++) {
            fin >> bit;
            if (bit == 1) { value += pow(2, i); }
        }
        graph.values.push_back(value);
        if (fin.eof()) { break; }
    };

    fin.close();

    return graph;
}

short hamming(int x, int y) {
    short distance = 0;
    int aux = x ^ y;
    while (aux) {
        ++distance;
        aux &= aux - 1;
    }
    return distance;
}

int clusters_at_distance(Graph graph, int max_dist) {
    UF clusters(graph.n);
    size_t i, j;
    short distance;

    for (i = 0; i < graph.n; i++) {
        for (j = 0; j < graph.n; j++) {
            distance = hamming(graph.values[i], graph.values[j]);
            if (distance < max_dist) {
                clusters.merge(i, j);
            }
        }
        if ((i + 1) % 5000 == 0) { cout << i << " Iterations" << endl; }
    }

    return clusters.size;
}

int main(int argc, char** argv) {

    Graph graph;

    if(argc!=2) {
        cout << "Please indicate a graph file" << endl;
        return 1;
    };

    graph = read_file(argv[1]);

    // for (size_t i = 0; i < graph.values.size(); i++) {
    //     cout << graph.values[i] << endl;
    // }
    // cout << hamming(graph.values[0], graph.values[1]) << endl;
    // cout << hamming(graph.values[3], graph.values[0]) << endl;
    cout << "Clusters to achieve max_distance of 3: " << clusters_at_distance(graph, 3) << endl;

    return 0;
}