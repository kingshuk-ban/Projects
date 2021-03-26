#pragma once

#include <vector>
#include <iostream>
#include <math.h>
#include "typedefs.h"

void reshape(DataMatrixT& data, int n_rows, int n_cols=1)
{
    for (int i = 0; i < n_rows; i++)
    {
        std::vector<double> row; 
        data.push_back(row);
        for (int j = 0; j < n_cols; j++)
        {
            data[i].push_back(0.0);
        }
    }
}

double sigmoid(const std::vector<double>& inputs, const std::vector<double>& wts)
{
    //std::cout << "Applying sigmoid on " << wts.size() << " inputs " << std::endl;
    double z = 0.0;
    for (int i = 0; i < inputs.size(); i++)
    {
        z += wts[i] * inputs[i];
    }
    z += wts[wts.size() -1];
    return (1.0/(1.0 + exp(-z)));
}

double sigmoid_derivative(double output)
{
    return output * (1.0 - output);
}

double relu(const std::vector<double>& inputs, const std::vector<double>& wts)
{
    //std::cout << "Applying relu on " << wts.size() << " inputs " << std::endl;
    double z = 0.0;
    for (int i = 0; i < inputs.size(); i++)
    {
        z += wts[i] * inputs[i];
    }
    z += wts[wts.size() - 1];
    return (z > 0.0) ? z : 0.0;
}

double relu_derivative(double output)
{
    return (output <= 0.0) ? 0.0 : 1.0;
}

double init_weight(int dummy)
{
    srand(10);
    double w = rand()/(double)(RAND_MAX);
    // std::cout << "Random number generated : " << w << std::endl;
    return w;
}

double init_weight_len(int size_of_layer)
{
    double w = init_weight(1);
    return w * sqrt(2.0/size_of_layer);
}
