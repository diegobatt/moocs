#include <algorithm>
#include <fstream>
#include <iostream>
#include <vector>
#include <utility>
#include <stack>


using namespace std;

typedef pair<int, int> Clause;
struct Node {
    vector<size_t> from;
    vector<size_t> to;
};
struct Graph {
    size_t n;
    vector<Node> nodes;
};

vector<Clause> read_file(const char * filename, size_t& N) {

    vector<Clause> clauses;
    Clause aux_clause;
    ifstream fin;

    fin.open(filename);

    if (!fin.is_open()) {
        cout << "Could not open file: " << filename << endl;
        return clauses;
    };

    fin >> N;
    cout << "We have " << N << " clauses and variables." << endl;

    while(fin >> aux_clause.first >> aux_clause.second) {
        clauses.push_back(aux_clause);
    };

    fin.close();

    return clauses;
}

Graph clauses2graph(const vector<Clause> &clauses, size_t N) {
    Graph g;
    size_t aux_from, aux_to;

    g.n = 2 * N;
    g.nodes.resize(g.n);

    for (size_t i = 0; i < N; i++) {
        if (clauses[i].first > 0) {
            if (clauses[i].second > 0) {
                g.nodes[clauses[i].first + N - 1].to.push_back(clauses[i].second - 1);
                g.nodes[clauses[i].second - 1].from.push_back(clauses[i].first + N - 1);
                g.nodes[clauses[i].second + N - 1].to.push_back(clauses[i].first - 1);
                g.nodes[clauses[i].first - 1].from.push_back(clauses[i].second + N - 1);
            }
            else {
                g.nodes[clauses[i].first + N - 1].to.push_back(-clauses[i].second + N - 1);
                g.nodes[-clauses[i].second + N - 1].from.push_back(clauses[i].first + N - 1);
                g.nodes[-clauses[i].second - 1].to.push_back(clauses[i].first - 1);
                g.nodes[clauses[i].first - 1].from.push_back(-clauses[i].second + N - 1);
            }
        } else {
            if (clauses[i].second > 0) {
                g.nodes[-clauses[i].first - 1].to.push_back(clauses[i].second - 1);
                g.nodes[clauses[i].second - 1].from.push_back(-clauses[i].first - 1);
                g.nodes[clauses[i].second + N - 1].to.push_back(-clauses[i].first + N - 1);
                g.nodes[-clauses[i].first + N - 1].from.push_back(clauses[i].second + N - 1);
            }
            else {
                g.nodes[-clauses[i].first - 1].to.push_back(-clauses[i].second + N - 1);
                g.nodes[-clauses[i].second + N - 1].from.push_back(-clauses[i].first - 1);
                g.nodes[-clauses[i].second - 1].to.push_back(-clauses[i].first + N - 1);
                g.nodes[-clauses[i].first + N - 1].from.push_back(-clauses[i].second - 1);
            }
        }
    }

    return g;
}

void dfs(
    Graph &g,
    vector<bool> &explored,
    stack<size_t> &order,
    size_t vertex=0,
    bool forward=true)
{

    vector<size_t> *edges;
    cout << vertex << endl;
    if (vertex == 1) {
        cout << "vertex es 1, edge: " << g.nodes[vertex].to[0] << endl;
    }

    if (explored[vertex]) {
        cout << vertex << " has been explored." << endl;
        return;
    }
    explored[vertex] = true;

    edges = forward ? &g.nodes[vertex].to : &g.nodes[vertex].from;

    for (auto it = edges->begin(); it < edges->end(); it++) {
        dfs(g, explored, order, *it, forward);
    }

    order.push(vertex);

}

vector<size_t> get_topological_order(Graph &g, bool forward=false) {
    vector<bool> explored(g.n, false);
    stack<size_t> order;
    vector<size_t> result;

    for (size_t i = 0; i < g.n; i++) {
        if (!explored[i])
            dfs(g, explored, order, i, forward);
    }

    while (!order.empty()) {
        result.push_back(order.top());
        order.pop();
    }
    
    return result;
}

vector<size_t> get_scc(Graph &g) {
    vector<bool> explored(g.n, false);
    vector<size_t> order, sccs(g.n);
    stack<size_t> conns;
    size_t scc=0;

    cout << "Getting inverse topological order..." << endl;
    order = get_topological_order(g, false);

    cout << "Getting SCCs..." << endl;

    for (auto it = order.begin(); it < order.end(); it++) {

        if (!explored[*it])
            dfs(g, explored, conns, *it, true);

        if (!conns.empty()) {
            while (!conns.empty()) {
                sccs[conns.top()] = scc;
                conns.pop();
            }
            scc++;
        }
    }

    return sccs;
}

bool check_2sat(vector<Clause> clauses, size_t N) {
    Graph g;
    vector<size_t> scc; 

    g = clauses2graph(clauses, N);
    scc = get_scc(g);

    for (size_t i = 0; i < N; i++) {
        if (scc[i] == scc[i+N]) {
            cout << "Both " << i << " and " << (i+N) << " belong to the same scc" << endl;
            return false;
        }
    }

    return true;
    
}

int main(int argc, char** argv) {

    vector<Clause> clauses;
    Graph g;
    size_t N;
    vector<size_t> order;

    if(argc!=2) {
        cout << "Please indicate a graph file" << endl;
        return 1;
    };

    clauses = read_file(argv[1], N);
    g = clauses2graph(clauses, N);
    // cout << "It is: " << endl << check_2sat(clauses, N) << "!!!!" << endl;
    // for (size_t i = 0; i < g.n; i++) {
    //     cout << "Node " << i << " has edges to: [";
    //     for (auto j = g.nodes[i].to.begin(); j < g.nodes[i].to.end(); j++) {
    //         cout << *j << ", ";
    //     }
    // cout << "\b\b]" << endl;
    // }
    
    order = get_topological_order(g, true);
    order = get_scc(g);
    for (size_t i = 0; i < order.size(); i++) {
        cout << order[i] << ", ";
    }
    cout << "\b" << endl;


    return 0;
}
