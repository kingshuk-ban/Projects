#pragma once

#include "Model.h"
#include "common.h"

static double lr_cost_function_(const DataMatrixT& y, const DataMatrixT& yhat)
{
    double cost = 0.0;
    for (int i = 0; i < y.size(); i++)
    {
        cost += pow((yhat[i][0] - y[i][0]), 2.0);
    }
    cost = cost / (2.0 * y.size());
    return cost;
}

static double logr_cost_function_(const DataMatrixT& y, const DataMatrixT& yhat)
{
    double cost = 0.0;
    for (int i = 0; i < y.size(); i++)
    {
        cost += -(y[i][0]*log(yhat[i][0])) - (1.0 - y[i][0])*log(1.0 - yhat[i][0]);
    }
    cost = cost / (1.0 * y.size());
    return cost;
}

static std::vector<double> lr_gradient_function_(const DataMatrixT& X, const DataMatrixT& y, const DataMatrixT& yhat)
{
    std::vector<double> gradients;
    gradients.resize(X[0].size() + 1); // includes bias as the last

    for (int row = 0; row < X.size(); row++)
    {
        for (int col = 0; col < X[row].size(); col++)
        {
            gradients[col] += (yhat[row][0] - y[row][0]) * X[row][col];
        }
        gradients[gradients.size() - 1] += (yhat[row][0] - y[row][0]);
    }
    for (int i = 0; i < gradients.size(); i++)
    {
        gradients[i] = gradients[i] / X.size();
    }
    return gradients;
}

class LinearRegression : public Model
{
    private:
        std::vector<double> weights_; 

        void update_weights(const std::vector<double>& gradients, double learning_rate_)
        {
            for (int i = 0; i < weights_.size(); i++)
            {
                weights_[i] = weights_[i] - learning_rate_ * gradients[i];
            }
        }

    public:
        LinearRegression(Model::type type=Model::type::REGRESSION, std::string name="LinearRegression") 
        : Model(type, name)
        {
        }

        ~LinearRegression()
        {
        }

        virtual void fit(const DataMatrixT& X, const DataMatrixT& y, double learning_rate_=0.1, int verbose=0) override
        {
            if (weights_.size() != X[0].size() + 1)
            {
                weights_.resize(X[0].size() + 1);
                for (int i = 0; i < weights_.size(); i++)
                {
                    weights_[i] = 0.0;
                }
                // this->print();
            }

            double prev_cost = 1000000000000.0; 
            double cost = prev_cost; 
            DataMatrixT yhat;
            reshape(yhat, y.size(), y[0].size());
            // std::cout << "yhat done" << "(" << yhat.size() << "," << yhat[0].size() << ")" << std::endl;
            int epoch = 0;
            while (cost <= prev_cost)
            {
                prev_cost = cost;
                this->predict(X, yhat);

                cost = (type_ == Model::type::REGRESSION) ? lr_cost_function_(y, yhat) : logr_cost_function_(y, yhat);

                auto gradients = lr_gradient_function_(X, y, yhat);
                this->update_weights(gradients, learning_rate_);
                if (verbose > 0)
                {
                    std::cout << "fit(): epoch " << epoch << " : cost " << cost << std::endl;
                }
                epoch++;
                if (epoch == 100000)
                {
                    std::cerr << "fit(): did not converge in 1000 iterations." << std::endl;
                }
            }
            std::cout << "fit() converged in " << epoch << " iterations. " << std::endl;

            is_fit_ = true;
        }

        virtual void predict(const DataMatrixT& X, DataMatrixT& preds) override
        {
            if (!is_fit_)
            {
                //std::cerr << "Error: The model has not been fit yet. Please call fit() before predict()." << std::endl;
                //return;
            }
            for (int row = 0; row < X.size(); row++)
            {
                double yhat = 0.0;
                for (int col = 0; col < X[row].size(); col++)
                {
                    yhat += X[row][col]*weights_[col];
                }
                yhat += weights_[weights_.size() - 1];
                if (type_ == Model::type::CLASSIFICATION)
                {
                    yhat = 1.0 / (1.0 + exp(-yhat));
                }
                preds[row][0] = yhat;
            }
        }

        virtual void print() override
        {
            std::cout << "LinearRegression weights: " << std::endl;
            for (int i = 0; i < weights_.size(); i++)
            {
                std::cout << " " << weights_[i]; 
            }
            std::cout << std::endl;
        }
};