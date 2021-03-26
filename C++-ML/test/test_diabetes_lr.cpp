#include <iostream>
#include <vector>
#include "datafile.h"
#include "LinearRegression.h"
#include "reporting.h"

int main()
{
    DataFile df("../datasets/pima-indians-diabetes.csv");

    // Read and process the data
    df.read(8, "\\s*,", 0);

    std::cout << "Shape of data: ";
    auto shape = df.shape(df.get_data()); 
    std::cout << std::get<0>(shape) << "," << std::get<1>(shape); 
    std::cout << std::endl;

    std::cout << "Head of the data read" << std::endl;
    df.head();

    std::cout << "Describing the data" << std::endl; 
    df.describe();

    // df.onehot_y();

    // Train and test split the data
    std::cout << "Train and test split" << std::endl;
    auto res = df.train_test_split(0.33);
    const DataMatrixT& X_train = std::get<0>(res);
    const DataMatrixT& Y_train = std::get<1>(res);
    const DataMatrixT& X_test = std::get<2>(res);
    const DataMatrixT& Y_test = std::get<3>(res);

    std::cout << "Train_test sizes: (" << X_train.size() << ", " << Y_train.size() << ", " 
            << X_test.size() << ", " << Y_test.size() << ")" << std::endl;
    
    // Scaling the train and test data
    std::cout << "Scale and print the train data" << std::endl;
    auto X_train_scaled = df.normalize(X_train);
    df.print(X_train_scaled, 10);

    // df.print(Y_train, 10);

    std::cout << "Scale and print the test data" << std::endl;
    auto X_test_scaled = df.normalize(X_test);
    df.print(X_test_scaled, 10);

    LinearRegression lr(Model::type::CLASSIFICATION);
    
    lr.fit(X_train_scaled, Y_train, 0.01, 0);
    lr.print();

    DataMatrixT preds;
    reshape(preds, Y_test.size(), Y_test[0].size());
    lr.predict(X_test_scaled, preds);
    std::cout << "Actual: " << std::endl;
    df.print(Y_test, 20);
    std::cout << "Predicted: " << std::endl;
    df.print(preds, 20);

    Report rep(ModeT::BINARY_CLASSIF, 2);
    rep.compare_print(Y_test, preds);
}
