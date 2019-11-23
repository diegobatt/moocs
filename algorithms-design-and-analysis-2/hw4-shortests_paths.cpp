#include <fstream>
#include <iostream>
#include <limits>
#include <vector>

using namespace std;

const int pinf = numeric_limits<int>::max();
const int ninf = numeric_limits<int>::min();

struct Edge {
    size_t from;
    size_t to;
    int length;
};

struct Graph {
    size_t n;
    size_t m;
    vector<Edge> edges;
};

Graph read_file(const char * filename) {

    Graph g;
    Edge aux_edge;
    ifstream fin;

    fin.open(filename);

    if (!fin.is_open()) {
        cout << "Could not open file: " << filename << endl;
        return g;
    };

    fin >> g.n >> g.m;
    cout << "We have " << g.n << " nodes and ";
    cout << g.m << " edges" << endl;

    while(fin >> aux_edge.from >> aux_edge.to >> aux_edge.length) {
        --aux_edge.from;
        --aux_edge.to;
        g.edges.push_back(aux_edge);
    };

    fin.close();

    return g;
}

int floyd_warshall_min(Graph g) {

    vector<int> aux_init(g.n, pinf);
    vector<vector<int> > old_A(g.n, aux_init);
    vector<vector<int> > new_A(g.n, aux_init);
    int min_value = pinf;

    // Further initialization
    for (size_t i = 0; i < g.n; i++) {
        old_A[i][i] = 0;
    }
    for(vector<Edge>::iterator it = g.edges.begin(); it != g.edges.end(); ++it) {
        old_A[it->from][it->to] = it->length;
    }

    for (size_t k = 0; k < g.n; k++) {
        if (k % (g.n / 10) == 0) {
            cout << k << " Iterations " << endl;
        }
        for (size_t i = 0; i < g.n; i++) {
            for (size_t j = 0; j < g.n; j++) {
                if (old_A[i][k] == pinf || old_A[k][j] == pinf) {
                     new_A[i][j] = old_A[i][j];
                } else {
                    new_A[i][j] = min(old_A[i][j], old_A[i][k] + old_A[k][j]);     
                }
            }
        }
        old_A = new_A;
    }

    // Negative loop check
    for (size_t i = 0; i < g.n; i++) {
        if (new_A[i][i] < 0) {
            cout << "Negative cycle!" << endl;
            return ninf;
        }
    }

    for (size_t i = 0; i < g.n; i++) {
        for (size_t j = 0; j < g.n; j++) {
            if (i != j) {
                min_value = min(min_value, new_A[i][j]);
            }
        }
    }

    return min_value;
}

int main(int argc, char** argv) {

    Graph g;
    int min_value;

    if(argc!=2) {
        cout << "Please indicate a graph file" << endl;
        return 1;
    };

    g = read_file(argv[1]);
    min_value = floyd_warshall_min(g);

    cout << "The min value is: " << min_value << endl;

    return 0;
}