#include <fstream>
#include <iostream>
#include <limits>
#include <vector>

using namespace std;

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
        g.edges.push_back(aux_edge);
    };

    fin.close();

    return g;
}

int floyd_warshall_min(Graph g) {

    int inf = numeric_limits<int>::max();
    vector<int> aux_init_0(g.n+1, inf);
    vector<vector<int> > aux_init_1(g.n+1, aux_init_0);
    vector<vector<vector<int> > > A(g.n+1, aux_init_1);
    int min_value = inf;

    // Further initialization
    for (size_t i = 1; i <= g.n; i++) {
        A[0][i][i] = 0;
    }
    for(vector<Edge>::iterator it = g.edges.begin(); it != g.edges.end(); ++it) {
        A[0][it->from][it->to] = it->length;
    }

    for (size_t k = 1; k <= g.n; k++) {
        for (size_t i = 1; i <= g.n; i++) {
            for (size_t j = 1; j <= g.n; j++) {
                if (A[k-1][i][k] == inf || A[k-1][k][j] == inf) {
                     A[k][i][j] = A[k-1][i][j];
                } else {
                    A[k][i][j] = min(A[k-1][i][j], A[k-1][i][k] + A[k-1][k][j]);     
                }
            }
        }
    }

    // Negative loop check
    for (size_t i = 1; i <= g.n; i++) {
        if (A[g.n][i][i] < 0) {
            cout << "Negative cycle!!!!!" << endl;
            return numeric_limits<int>::min();
        }
    }

    for (size_t i = 1; i <= g.n; i++) {
        for (size_t j = 1; j <= g.n; j++) {
            if (i != j) {
                min_value = min(min_value, A[g.n][i][j]);
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