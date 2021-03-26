#include <iostream>
#include <vector>
#include "neural_network.h"
#include "LinearRegression.h"
#include "datafile.h"
#include "reporting.h"

int main(int argc, char* argv[])
{
    double l_rate = (argc > 1) ? atof(argv[1]) : 0.05;
    int n_epochs = (argc > 2) ? atoi(argv[2]) : 1000;

    DataFile df("../datasets/pima-indians-diabetes.csv");

    // Read and process the data
    df.read(8, "\\s*,", 0);
    df.head();
    df.describe();
    // df.onehot_y();
    
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
    std::cout << "Y_train" << std::endl;
    df.print(Y_train, 10);
    std::cout << "Y_test" << std::endl;
    df.print(Y_test, 10);
    // exit(0);
    auto X_test_scaled = df.normalize(X_test);

    // Build the network
    
    Network network(1.0);
    network.addInput(8, 12, sigmoid, sigmoid_derivative);
    network.addHidden(8, sigmoid, sigmoid_derivative);
    //network.addHidden(7, sigmoid, sigmoid_derivative);
    network.addOutput(1, sigmoid, sigmoid_derivative);

    // Train the network
    network.train(l_rate, n_epochs, X_train_scaled, Y_train);
    network.print_weights();

    // Predict on test data
    std::vector<std::vector<double> > preds;
    network.predict(X_test_scaled, preds);

    Report nn_report(ModeT::BINARY_CLASSIF, 2);
    nn_report.compare_print(Y_test, preds);
    
    DataMatrixT lr_preds; 
    reshape(lr_preds, Y_test.size(), Y_test[0].size());

    LinearRegression lr;
    lr.fit(X_train_scaled, Y_train, 0.01, 0);
    lr.print();

    lr.predict(X_test_scaled, lr_preds);

    // How did we do?
    Report lr_report(ModeT::BINARY_CLASSIF, 2);
    lr_report.compare_print(Y_test, lr_preds);
}
