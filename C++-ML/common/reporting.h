#pragma once
#include <iostream>
#include <iomanip>
#include "common.h"
#include "../variadic_table-master/include/VariadicTable.h"

enum class ModeT 
{
        BINARY_CLASSIF = 0,
        MULTI_CLASSIF = 1,
        REGRESSION = 2
}; 

class Report
{
    private:
        ModeT mode; // true: classification (default), false: regression
        int num_classes;

        // binary classification metrics
        int true_pos;
        int true_neg;
        int false_pos;
        int false_neg;

        // actual/prediction counts for multi-class
        std::vector<std::vector<int> > multi_class_metrics;

        float accuracy;
        float precision;
        float recall;

        // regression metrics
        float mean_absolute_error;
        float mean_squared_error; 
        float root_mean_squared_error; 
    
        int decodeClass(const std::vector<double>& outputs) const
        {
            if (outputs.size() == 1) // binary class
            {
                return (outputs[0] < 0.5)? 0 : 1;
            }
            
            int p = -1;
            double max = -1;
            for (int i = 0; i < outputs.size(); i++)
            {
                if (outputs[i] > max)
                {
                    max = outputs[i];
                    p = i;
                }
            }
            return p;
        }

        const std::string getMode()
        {
            switch(mode)
            {
                case ModeT::BINARY_CLASSIF: return "BINARY"; 
                case ModeT::MULTI_CLASSIF: return "MULTICLASS";
                case ModeT::REGRESSION: return "REGRESSION";
            }
        }

        void classif_compare(const DataMatrixT& actual, const DataMatrixT& predicted)
        {
            double score = 0.0;
            for (int i = 0; i < actual.size(); i++)
            {
                int y = decodeClass(actual[i]);
                int p = decodeClass(predicted[i]);
                if ((y == 0) && (p == 0))
                    true_neg++;
                if ((y == 1) && (p == 1))
                    true_pos++;
                if ((y == 0) && (p == 1))
                    false_pos++;
                if ((y == 1) && (p == 0))
                    false_neg++;
            }
            accuracy = float(true_pos + true_neg) / float(true_pos + true_neg + false_pos + false_neg);
            precision = float(true_pos) / float(true_pos + false_pos);
            recall = float(true_pos) / float(true_pos + false_neg);
        }

        void classif_multi_compare(const DataMatrixT& actual, const DataMatrixT& predicted)
        {
            for (int i = 0; i < actual.size(); i++)
            {
                int y = decodeClass(actual[i]);
                int p = decodeClass(predicted[i]);
                multi_class_metrics[y][p] += 1;
                if (y == p)
                {
                    accuracy++;
                }
            }
            accuracy = float(accuracy) / float(actual.size());
        }
        
        void calculate_regression_metrics(const DataMatrixT& actual, const DataMatrixT& predicted)
        {
            double abserror = 0.0;
            double sqerror = 0.0;
            for (int i = 0; i < actual.size(); i++)
            {
                // Need to extend this for multiple classes
                double y = actual[i][0];
                double yhat = predicted[i][0];
                abserror += abs(y - yhat);
                sqerror += pow((y - yhat), 2.0);
            }
            mean_absolute_error = abserror/actual.size();
            mean_squared_error = sqerror/actual.size();
            root_mean_squared_error = sqrt(mean_squared_error); 
        }

    public:
    /*
        Report(ModeT mode=ModeT::REGRESSION): mode(mode), num_classes(0),
            true_pos(0), true_neg(0), false_pos(0), false_neg(0),
            accuracy(0.0), precision(0.0), recall(0.0),
            mean_absolute_error(0.0), mean_squared_error(0.0)
        {

        }
    */

        Report(ModeT mode = ModeT::BINARY_CLASSIF, int num_classes=2) : mode(mode), num_classes(num_classes),
            true_pos(0), true_neg(0), false_pos(0), false_neg(0),
            accuracy(0.0), precision(0.0), recall(0.0),
            mean_absolute_error(0.0), mean_squared_error(0.0)
        {
            std::cout << "Report opended in " << getMode() << " mode for " << num_classes << " classes." << std::endl;
            for (int i = 0; i < num_classes; i++)
            {
                std::vector<int> row;
                multi_class_metrics.push_back(row);
                for (int j = 0; j < num_classes; j++)
                {
                    multi_class_metrics[i].push_back(0);
                }
            }
        }

        void compare_print(const DataMatrixT& actual, const DataMatrixT& predicted)
        {
            if (mode == ModeT::BINARY_CLASSIF)
            {
                classif_compare(actual, predicted);
                std::cout << "Accuracy : " << accuracy << std::endl;
                std::cout << "Precision : " << precision << std::endl;
                std::cout << "Recall : " << recall << std::endl;
                std::cout << "F1-score : " << (precision*recall*2)/(precision + recall) << std::endl;
                std::cout << "Confusion Matrix:" << std::endl;

                VariadicTable<std::string, int, int> vt({"Actual/Predicted", "Actual True", "Actual False"}, 10);
                vt.addRow("Predicted True", true_pos, false_pos); 
                vt.addRow("Predicted False", false_neg, true_neg);
                vt.print(std::cout);
            }
            else if (mode == ModeT::MULTI_CLASSIF)
            {
                classif_multi_compare(actual, predicted);
                std::cout << "Accuracy : " << accuracy << std::endl;
                std::cout << "Confusion Matrix: (actual-predicted) " << std::endl;
                for (int i = 0; i < multi_class_metrics.size(); i++)
                {
                    for (int j = 0; j < multi_class_metrics[i].size(); j++)
                    {
                        std::cout << std::setw(5) << i << "-" << j << " : " << std::setw(5) << multi_class_metrics[i][j] << " "; 
                    }
                    std::cout << std::endl;
                }
            }
            else if (mode == ModeT::REGRESSION)
            {
                calculate_regression_metrics(actual, predicted);
                std::cout << "Mean Absolute Error: " << mean_absolute_error << std::endl;
                std::cout << "Mean Squared Error:  " << mean_squared_error << std::endl; 
                std::cout << "Root Mean Squared Error: " << root_mean_squared_error << std::endl; 
            }
        }
};
