#include <algorithm>
#include <fstream>
#include <iostream>
#include <limits>
#include <vector>
#include <cmath>
#include <set>

using namespace std;

const float pinf = numeric_limits<float>::max();

struct Graph {
    size_t n;
    vector<vector<float> > edges;
};

Graph read_file(const char * filename) {

    Graph g;
    float x, y;
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
        g.edges.push_back(ds);
    }
    
    fin.close();

    return g;
}

vector<set<set<size_t> > > get_powerset(size_t n, bool include_zero=true) {

    set<size_t> aux_set;
    short start = (short) include_zero;
    vector<set<set<size_t> > > subsets(n - start);
    size_t cardinality = pow(2, n - start);

    for(size_t i = 0; i < cardinality; i++) {

        if ( i % 100000 == 0)
            cout << i << " Iterations of " << cardinality << endl; 

        for(size_t j = 0; j < n - start ; j++) { 
            if(i & (1 << j)) aux_set.insert(j + start);
        }
        if (aux_set.size())
            subsets[aux_set.size() - start].insert(aux_set);
        aux_set.clear();
    }
    return subsets;
}

void print_powerset(vector<set<set<size_t> > > powerset, bool include_zero=true) {

    short start = (short) include_zero;

    for (size_t i = 0; i < powerset.size(); i++) {
        cout << " Sets with cardinality " << i + start << ": ";
        for (auto it = powerset[i].begin(); it != powerset[i].end(); ++it) {
            cout << "{";
            for (auto jt = it->begin(); jt != it->end(); ++jt) {
                cout << *jt << ", ";
            }
            cout << "}, ";
        }
        cout << endl;
    }
}

float min_tsp(Graph g) {

    size_t cardinality = pow(2, g.n - 1); // Cardinality of al sets that include 0
    vector<set<set<size_t> > > powerset;
    vector<float> aux_init(cardinality, pinf);
    vector<vector<float> > A(g.n, aux_init);
    size_t seq, sub_seq; 
    float aux_min;

    A[0][0] = 0;
    powerset = get_powerset(g.n);

    for (size_t i = 0; i < powerset.size(); i++) {

        if ( i % 100000 == 0)
            cout << i << " Iterations of " << cardinality << endl; 

        for (auto it = powerset[i].begin(); it != powerset[i].end(); it++) {

            seq = 0;
            for (auto jt = it->begin(); jt != it->end(); jt++) {
                seq += pow(2, *jt - 1);
            }

            for (auto jt = it->begin(); jt != it->end(); jt++) {

                sub_seq = seq - pow(2, *jt - 1);

                if (it->size() == 1) {
                    A[*jt][seq] = g.edges[0][*jt];
                    continue;
                }

                aux_min = pinf;
                for (auto kt = it->begin(); kt != it->end(); kt++) {

                    if (*kt != *jt)
                        aux_min = min(
                            aux_min,
                            A[*kt][sub_seq] + g.edges[*kt][*jt]);
                }

                A[*jt][seq] = aux_min;
            }
        }
    }

    aux_min = pinf;
    for (size_t i = 1; i < g.n; i++) {
        aux_min = min(aux_min, A[i][cardinality-1] + g.edges[i][0]);
    }

    return aux_min;
}

int main(int argc, char** argv) {

    Graph g;
    float min_cost;
    vector<set<set<size_t> > > powerset;

    if(argc!=2) {
        cout << "Please indicate a graph file" << endl;
        return 1;
    };

    g = read_file(argv[1]);
    // cout << "Getting powerset..." << endl;
    // powerset = get_powerset(g.n);
    // print_powerset(powerset);
    cout << "Powerset calculated..." << endl;
    min_cost = min_tsp(g);
    cout << min_cost << endl;

    return 0;
}