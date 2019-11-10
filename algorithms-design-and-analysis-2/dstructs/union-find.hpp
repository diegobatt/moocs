#ifndef UF_H
#define UF_H

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
                nodes[rewires[i]].parent = root;
            };

            return root;
        };

        void merge(int v, int w) {
            int root_v = find(v);
            int root_w = find(w);
            if (root_v == root_w) { return; } 
            if (nodes[root_v].rank <= nodes[root_w].rank) {
                if (nodes[root_v].rank == nodes[root_w].rank) {
                    nodes[root_v].rank++;
                };
                nodes[root_w].parent = root_v;
            } else {
                nodes[root_v].parent = root_w;
            };
            size--;
        };
};

#endif