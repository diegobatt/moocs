#include <vector>
#include <iostream>
#include <fstream>

using namespace std;

struct Element {
    int weight;
    int value;
};

vector<Element> read_file(const char * filename, int * W, int * N) {

    vector<Element> elements;
    Element aux_element;
    ifstream fin;

    fin.open(filename);

    if (!fin.is_open()) {
        cout << "Could not open file: " << filename << endl;
        return elements;
    };

    fin >> *W >> *N;
    cout << "We have a bag of size " << *W << " and ";
    cout << *N << " elements" << endl;

    while(fin >> aux_element.value >> aux_element.weight) {
        elements.push_back(aux_element);
    };

    fin.close();

    return elements;
}

int optimal_knapsack(vector<Element> elements, int W, int N) {

    vector<vector<int>> A(N);

    for (size_t i = 0; i < N; i++) {
        for (size_t j = 0; j < W + 1; j++) {
            if (i == 0) {
                A[i].push_back(0);
            } else if (j < elements[i].weight) {
                A[i].push_back(A[i-1][j]);
            } else {
                A[i].push_back(max(
                    A[i-1][j],
                    A[i-1][j-elements[i].weight] + elements[i].value));
            }
        }
    }
    return A[N-1][W];
}

int main(int argc, char** argv) {

    vector<Element> elements;
    int N, W, optimal;

    if(argc!=2) {
        cout << "Please indicate a graph file" << endl;
        return 1;
    };

    elements = read_file(argv[1], &W, &N);

    optimal = optimal_knapsack(elements, W, N);
    cout << "The optimum is " << optimal << endl;
    
    return 0;
}
