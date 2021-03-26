#include "Model.h"
#include <math.h>

void Model::fit(const DataMatrixT& X, const DataMatrixT& y)
{
    // this is naive fit for regression or classification
    // So it does not use the X vector at all. 
    int number_of_outputs = y[0].size();
    predicted_ = new DataVectorT(number_of_outputs);

    for (int row = 0; row < y.size(); row++)
    {
        for (int col = 0; col < y[row].size(); col++)
        {
            predicted_[col] += y[row][col];
        }
    }
    for (int col; col < number_of_outputs; col++)
    {
        predicted_[col] = predicted_[col] / y.size(); 
    }
    is_fit_ = true;
}

void Model::predict(const DataMatrixT& X, DataMatrixT& pred)
{
    if (!is_fit_)
    {
        std::cerr << "Error: The model has not been fit yet. Please call fit() before predict()." << std::endl;
        return;
    }
    
    for (int row = 0; row < X.size(); row++)
    {
        for (int col = 0; col < pred[row].size(); col++)
        {
            pred[row][col] = predicted_[col];
        }
    }
}

double Model::score(const DataMatrixT& X, const DataMatrixT& y)
{
    fit(X, y);
    double score = 0.0;
    for (int i = 0; i < y.size(); i++)
    {
        for (int j = 0; j < y[i].size(); j++)
        {
            score += pow((y[i][j] - predicted_[j]), 2.0);
        }
    }
    score = score / y.size();
    return score; 
}

void Model::print()
{
    std::cout << "***************************************************************************************************" << std::endl;

    std::cout << "Model name: " << name_ << " type: " << (type_ == Model::type::REGRESSION) ? "REGRESSION" : "CLASSIFICATION" << std::endl; 
    if (is_fit_)
    {
        std::cout << "The model has been fit and learned."
    }
    else
    {
        std::cout << "The model has not been fit and ignorant."
    }
    
    std::cout << "***************************************************************************************************" << std::endl;
}