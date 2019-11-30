#include <algorithm>
#include <fstream>
#include <iostream>
#include <limits>
#include <vector>
#include <cmath>
#include <set>


using namespace std;

const float pinf = numeric_limits<float>::infinity();

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

void _get_perms(
    vector<vector<size_t> >& ans,
    vector<size_t>& tmp,
    size_t n,
    size_t left,
    size_t k) {

    if (k == 0) { 
        ans.push_back(tmp); 
        return;
    }

    for (size_t i = left; i <= n; ++i) { 
        tmp.push_back(i); 
        _get_perms(ans, tmp, n, i + 1, k - 1); 
        tmp.pop_back(); 
    } 
} 

vector<vector<size_t> > get_perms(size_t n, size_t k) { 
    vector<vector<size_t> > ans; 
    vector<size_t> tmp;
    _get_perms(ans, tmp, n, 1, k); 
    return ans; 
}

void print_perms(const vector<vector<size_t> > &perms) {
    for (size_t i = 0; i < perms.size(); i++) { 
        for (size_t j = 0; j < perms[i].size(); j++) { 
            cout << perms.at(i).at(j) << " "; 
        } 
        cout << endl; 
    } 
}

float min_tsp(Graph g) {

    size_t cardinality = pow(2, g.n - 1); // Cardinality of al sets that include 0
    vector<vector<size_t> > perms;
    vector<float> aux_init(cardinality, pinf);
    vector<vector<float> > A(g.n, aux_init);
    size_t seq, sub_seq; 
    float aux_min;

    A[0][0] = 0;

    for (size_t i = 1; i < g.n; i++) {
        cout << i << " Iterations of " << g.n - 1 << endl;
        perms = get_perms(g.n - 1, i);

        for (auto it = perms.begin(); it != perms.end(); it++) {

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
                        if (A[*kt][sub_seq] < pinf) {
                            aux_min = min(
                                aux_min,
                                A[*kt][sub_seq] + g.edges[*kt][*jt]);
                        }
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
    vector<vector<size_t> > perms;

    if(argc!=2) {
        cout << "Please indicate a graph file" << endl;
        return 1;
    };

    g = read_file(argv[1]);
    min_cost = min_tsp(g);
    cout << min_cost << endl;

    return 0;
}