#include <iostream>
#include <fstream>
#include <algorithm>
#include <vector>

using namespace std;

struct UFNode {
    size_t parent;
    size_t rank;
};

class UF {

    private:
        vector<UFNode> nodes;

    public:
        int size;
 
        UF(int N) {
            UFNode aux_node;
            size_t i;
            for (i=0; i<N; i++) {
                aux_node = {i, 0};
                nodes.push_back(aux_node);
            };
            size = N;
        };

        int find(int v) {
            int root = v;
            vector<int> rewires;
            size_t i;

            while (nodes[root].parent != root) {
                rewires.push_back(root);
                root = nodes[root].parent;
            };
            for(i=0; i<rewires.size(); i++){
                nodes[i].parent = root;
            };

            return root;
        };

        void merge(int v, int w) {
            int root_v = find(v);
            int root_w = find(w);

            if (nodes[root_v].rank <= nodes[root_w].rank) {
                cout << root_v << " rank " << nodes[root_v].rank << endl;
                cout << root_w << " rank " << nodes[root_w].rank << endl;
                if (nodes[root_v].rank == nodes[root_w].rank) {
                    nodes[root_v].rank++;
                    cout << root_v << " updated rank  " << nodes[root_v].rank << endl;
                };
                nodes[root_w].parent = root_v;
            } else {
                nodes[root_v].parent = root_w;
            };
            size--;
        };
};

int main() {
    int N = 4;
    UF uf(N);

    // cout << uf.find(0) << endl;
    // cout << uf.find(1) << endl;
    // cout << uf.find(2) << endl;
    // cout << uf.find(3) << "first" << endl;
    uf.merge(0, 1);
    // cout << uf.find(0) << endl;
    // cout << uf.find(1) << "second" << endl;
    uf.merge(3, 2);
    // cout << uf.find(2) << endl;
    // cout << uf.find(3) << endl;
    // cout << uf.find(0) << "third" << endl;
    uf.merge(0, 2);
    // cout << uf.find(0) << endl;
    // cout << uf.find(1) << endl;
    cout << uf.find(2) << endl;
    // cout << uf.find(3) << "fourth" << endl;

};
