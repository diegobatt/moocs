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
    Graph g,
    vector<size_t> &order,
    vector<bool> &explored,
    size_t vertex=0,
    bool forward=true)
{
    vector<size_t> *edges;

    if (explored[vertex])
        return;
    explored[vertex] = true;

    edges = forward ? &g.nodes[vertex].to : &g.nodes[vertex].from;

    for (auto i = edges->begin(); i < edges->end(); i++) {
        
    }
     


        


}

int main(int argc, char** argv) {

    vector<Clause> clauses;
    Graph g;
    size_t N;

    if(argc!=2) {
        cout << "Please indicate a graph file" << endl;
        return 1;
    };

    clauses = read_file(argv[1], N);
    g = clauses2graph(clauses, N);

    for (size_t i = 0; i < g.n; i++) {
        cout << "Node " << i << " has edges to: [";
        for (auto j = g.nodes[i].to.begin(); j < g.nodes[i].to.end(); j++) {
            cout << *j << ", ";
        }
    cout << "\b\b]" << endl;
    }
    
    return 0;
}
