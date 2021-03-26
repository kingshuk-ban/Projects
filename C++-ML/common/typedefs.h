#pragma once

#include <vector>
#include <functional>

// Data types to handle X and Y vectors
typedef std::vector<std::vector<double> > DataMatrixT;
typedef std::vector<double> DataVectorT;

typedef struct {
    std::string type;
    double min;
    double max;
    double mean;
    double median;
    double percent_25;
    double percent_75;
    int n_entries; 
} ColumnStatistics; 

// Function prototypes
std::function<double(double)> ActivationFunction;
std::function<double(double)> ActivationDerivativeFunction;
std::function<double(double)> RandomFunc;

std::function<double(const DataMatrixT& y, const DataMatrixT& yhat)> CostFunction; 

std::function<DataMatrixT(const DataMatrixT& data)> TransformMatrixFunction;
std::function<DataVectorT(const DataVectorT& data)> TransformVectorFunction;




