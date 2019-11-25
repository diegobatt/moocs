#include <fstream>
#include <iostream>
#include <limits>
#include <vector>
#include <cmath>

using namespace std;

const int pinf = numeric_limits<float>::max();

struct Graph {
    size_t n;
    vector<vector<float> > A;
};

Graph read_file(const char * filename) {

    Graph g;
    vector<float> xs, ys, ds;
    ifstream fin;

    fin.open(filename);

    if (!fin.is_open()) {
        cout << "Could not open file: " << filename << endl;
        return g;
    };

    fin >> g.n;
    cout << "We have " << g.n << " Cities." << endl;

    while(fin >> x >> y) {
        xs.push_back(x);
        ys.push_back(y);
    };

    ds.resize(g.n);
    for (size_t i = 0; i < g.n; i++) {
        for (size_t j = 0; j < g.n; j++) {
            ds[j] = sqrt(pow(xs[i] - xs[j], 2) + pow(ys[i] - ys[j], 2));
        }
        g.A.push_back(ds);
    }
    
    fin.close();

    return g;
for
}

float min_tsp(Graph g) {

    size_t cardinality = pow(2, g.n);
    vector<float> aux_init(cardinality, pinf);
    vector<vector<float> > A(g.n, aux_init);
    A[0][0] = 0;

    for (size_t n = 1; n < g.n; n++) {
        for (size_t c = 0; c < pow(2, n); c++) {
            for (size_t i = 0; i < ; i++) {

            }
        }
    }
    

    return 1.1
}

int main(int argc, char** argv) {

    Graph g;
    float min_cost;

    if(argc!=2) {
        cout << "Please indicate a graph file" << endl;
        return 1;
    };

    g = read_file(argv[1]);
    min_cost = min_tsp(g);

    cout << "The min value is: " << min_cost << endl;

    return 0;
}