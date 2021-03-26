#include <iostream>
#include <vector>
#include "neural_network.h"
#include "datafile.h"
#include "reporting.h"

int main()
{
    DataFile df("../datasets/seeds_dataset.csv");

    // Read and process the data
    df.read(7);
    df.head();
    df.describe();
    df.onehot_y();

    // Train and test split the data
    auto res = df.train_test_split(0.7);
    const DataMatrixT& X_train = std::get<0>(res);
    const DataMatrixT& Y_train = std::get<1>(res);
    const DataMatrixT& X_test = std::get<2>(res);
    const DataMatrixT& Y_test = std::get<3>(res);
    std::cout << "Train_test sizes: (" << X_train.size() << ", " << Y_train.size() << ", " 
            << X_test.size() << ", " << Y_test.size() << ")" << std::endl;
    
    // Scaling the train and test data
    auto X_train_scaled = df.normalize(X_train);
    df.print(X_train_scaled, 10);
    df.print(Y_train, 10);

    auto X_test_scaled = df.normalize(X_test);

    // Build the network
    auto act_fn = sigmoid;
    auto act_fn_deriv = sigmoid_derivative;

    Network network(1.0);
    network.addInput(7, 10, act_fn, act_fn_deriv);
    network.addHidden(10, act_fn, act_fn_deriv);
    network.addHidden(7, act_fn, act_fn_deriv);
    network.addOutput(3, sigmoid, sigmoid_derivative);

    // Train the network
    network.train(0.5, 10000, X_train_scaled, Y_train);

    // Predict on test data
    std::vector<std::vector<double> > preds;
    network.predict(X_test_scaled, preds);

    // How did we do?
    double accuracy=network.compare(Y_test, preds);
    std::cout << "Accuracy: " << accuracy << "%" << std::endl; 
    network.print_weights();

    Report report(ModeT::MULTI_CLASSIF, 3);
    report.compare_print(Y_test, preds);
}
