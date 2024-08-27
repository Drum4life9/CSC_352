#include <iostream>
#include <vector>
#include <tuple>
#include <string>
#include <fstream>
#include <random>
#include <numeric>


using namespace std;

vector<double> train_classifer(vector<vector<double>> & pairs) {

    random_device rd;
    default_random_engine e(rd());
    uniform_int_distribution<int> ui(0, pairs.size() - 1);

    int step = 1;

    vector<double> weights = {1,1,1};

    while (step <= 5000000) {
        double alpha = (1000 * 1.0)/(1000+step);

        //choose an example at random
        int ex_num = ui(e);
        vector<double> example = pairs[ex_num];

        vector<double> x = {1, example[0], example[1]};

        double dot = inner_product(weights.begin(), weights.end(), x.begin(), 0);

        double h_num = 1/(1 + exp(-1 * dot));
        double loss_stuff = ((example[2] - h_num) * h_num * (1 - h_num));

        for (int i = 0; i < 3; ++i) {
            double weight_i = weights[i] + alpha * loss_stuff * x[i];
            weights[i] = weight_i;
        }


        step++;
    }



    return weights;
}

int main() {
    vector<vector<double>> points;

    string inp = "";
    ifstream file;

    file.open("../points.txt");

    while (getline(file, inp)) {
        double x = stod(inp.substr(0, inp.find(' ')));
        inp = inp.substr(inp.find(' ') + 1);
        double y = stod(inp.substr(0, inp.find(' ')));
        int ans = stoi(inp.substr(inp.find(' ') + 1));

        vector<double> pair = {x, y, ans * 1.0};

        points.emplace_back(pair);
    }

    vector<double> test = train_classifer(points);

    cout << test[0]  << " " << test[1] << " " << test[2] << endl;
}
