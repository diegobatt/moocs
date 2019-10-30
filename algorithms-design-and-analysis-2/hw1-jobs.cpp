#include <iostream>
#include <fstream>
#include <algorithm>
#include <vector>
#include <string>

using namespace std;

struct Job {
    size_t length;
    size_t weight;
};

vector<Job> read_file(const char * filename) {

    int n;
    Job aux_job;
    vector<Job> jobs;
    ifstream fin;

    fin.open(filename);

    if (!fin.is_open())
    {
        cout << "Could not open file: " << filename << endl;
        return jobs;
    }

    fin >> n;
    cout << "We have " << n << " Columns" << endl;

    while(fin >> aux_job.weight >> aux_job.length) {
        jobs.push_back(aux_job);
    };

    fin.close();

    return jobs;
};

bool diff_cmp(Job left, Job right) {
    int left_score = left.weight - left.length;
    int right_score = right.weight - right.length;

    if (left_score < right_score) {
        return false;
    } else if (left_score > right_score) {
        return true;
    } else {
        if (left.weight > right.weight) {
            return true;
        } else {
            return false;
        };
    };
};

bool ratio_cmp(Job left, Job right) {
    float left_score = (float)left.weight / (float)left.length;
    float right_score = (float)right.weight / (float)right.length;

    if (left_score < right_score) {
        return false;
    } else {
        return true;
    };
};

int main(int argc, char** argv)
{
    vector<Job> jobs;
    size_t i = 0, cum_length = 0, total=0;
    string cmp_argument;

    if(argc!=3) {
        cout << "difference or ratio comparator?" << endl;
        return 1;
    }

    cmp_argument = argv[2];
    jobs = read_file(argv[1]);

    if (cmp_argument == "ratio") {
        sort(jobs.begin(), jobs.end(), ratio_cmp);
    } else if (cmp_argument == "difference") {
        sort(jobs.begin(), jobs.end(), diff_cmp);
    } else {
        cout << "Second argument should be 'difference' or 'ratio'" << endl;
        return 1;      
    };

    for(i=0; i<jobs.size(); i++){
        cum_length += jobs[i].length;
        total += jobs[i].weight * cum_length;
    };

    cout << total << "\n";

    return 0;
}