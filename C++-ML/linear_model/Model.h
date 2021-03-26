/*
* This is the base class for all models.
* It can also be used as a baseline model to give naive predictions.
*/ 
#pragma once
#include <string>
#include "datafile.h"

class Model 
{
    public: 
    enum class type {
        REGRESSION, 
        CLASSIFICATION
    }; 

    protected:
        Model::type type_; 
        std::string name_;
        bool is_fit_;

    public:
        Model(Model::type typeofmodel, std::string name="unnamed")
        : type_(typeofmodel), name_(name), is_fit_(false)
        {
        }

        virtual ~Model()
        {
        }

        virtual void fit(const DataMatrixT& X, const DataMatrixT& y, double learning_rate=0.1, int verbose=0) = 0; 
        virtual void predict(const DataMatrixT& X, DataMatrixT& preds) = 0;
        // virtual double score(const DataMatrixT& X, const DataMatrixT& y) = 0;
        virtual void print() = 0;
};