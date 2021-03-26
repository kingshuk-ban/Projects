#pragma once 

#include <string>
#include <fstream>
#include <vector>
#include <set>
#include <map>
#include <regex>
#include <iostream>
#include <sstream>
#include <math.h>
#include "typedefs.h"

void _DEBUG_(const std::string& stage, const std::string& text)
{
    return;
    std::cout << "DEBUG: <" << stage << "> " << text << std::endl;
}

class DataFile
{
    private:
        // Store statistics of a column
        typedef struct {
            double min; double max; double sum;
            double mean; double std;
            double q1; double q2; double q3;
        } ColumnStatistics;

        // Store the data in original and transpose form
        DataMatrixT data; 
        DataMatrixT data_transpose;

        // Cut out the target columns
        DataMatrixT Y; // for multi-class data

        // Used in return from functions
        DataMatrixT emptyMatrix;
        DataVectorT emptyVector;

        // Column headers and statistics
        std::vector<ColumnStatistics> col_stats;
        std::map<std::string, int> col_names_to_index;
        std::vector<std::string> col_names_vector;

        // Input file (csv)
        std::string filename;
        std::ifstream fp;

        // Print spacing
        int _spacing; 

    private:
        // Column statistics helper functions
        void calculate_min_max_sum(const DataVectorT& col, int index)
        {
            col_stats[index].min = 0xffffffffffffffff;
            col_stats[index].max = -0xffffffffffffffff;

            for (auto v: col)
            {
                col_stats[index].min = (v < col_stats[index].min) ? v : col_stats[index].min;
                col_stats[index].max = (v > col_stats[index].max) ? v : col_stats[index].max;
                col_stats[index].sum += v; 
            }
        }

        void calculate_mean_std(const DataVectorT& col, int index)
        {
            col_stats[index].mean = col_stats[index].sum / col.size();
            col_stats[index].std = 0.0;
            for (auto v: col)
            {
                col_stats[index].std += pow((v - col_stats[index].mean), 2.0);
            }
            col_stats[index].std = sqrt(col_stats[index].std/(col.size() - 1));
        }

        void calculate_quartiles(const DataVectorT& col, int index)
        {
            DataVectorT temp = col;
            std::sort(temp.begin(), temp.end()); 
            int size = temp.size();
            int q2_index = (size + 1)/2;
            int q1_index = (q2_index + 1)/2;
            int q3_index = q2_index + q1_index;

            col_stats[index].q1 = temp[q1_index];
            col_stats[index].q2 = temp[q2_index];
            col_stats[index].q3 = temp[q3_index];
        }

        void calculate_column_stats()
        {
            _DEBUG_("calculate_column_stats", "START");
            int index = 0;
            for (auto col: data_transpose)
            {
                _DEBUG_("calculate stats", "START");
                col_stats.push_back(ColumnStatistics());
                calculate_min_max_sum(col, index);
                calculate_mean_std(col, index);
                calculate_quartiles(col, index);
                 _DEBUG_("calculate stats", "END");
                index++;
            }
            _DEBUG_("calculate_column_stats", "END");
        }

    public:
        // Constructor
        DataFile(const std::string& f)
        {
            fp.open(f, std::ifstream::in);
            _spacing = 10; 
        }

        // Destructor
        ~DataFile()
        {
            fp.close();
            for (int i = 0; i < data.size(); i++)
            {
                data[i].clear();
            }
            data.clear();
            for (int i = 0; i < data_transpose.size(); i++)
            {
                data_transpose[i].clear();
            }
            data_transpose.clear();
            col_stats.clear();
            col_names_to_index.clear();
            col_names_vector.clear();
        }

        const DataMatrixT& get_data() const 
        {
            return data;
        }

        const DataMatrixT& get_y() const
        {
            return Y;
        }

        void set_spacing(int num)
        {
            _spacing = num;
        }

        const DataVectorT& getColumn(const std::string& col)
        {
            auto it = col_names_to_index.find(col);
            if (it != col_names_to_index.end())
            {
                int index = (*it).second;
                return data_transpose[index];
            }
            return emptyVector;
        }

        void head(int n=10) const
        {
            if (col_names_vector.size())
            {
                std::cout << std::endl;
                for (auto n: col_names_vector)
                {
                    std::cout << std::setw(_spacing) << n << " ";
                }
                std::cout << std::endl;
            }

            int numrows = 0;
            for (auto row: data)
            {
                numrows++;
                for (auto col: row)
                {
                    std::cout << std::setw(_spacing) << col << " ";
                }
                std::cout << std::endl;
                if ((n != -1) && (numrows == n))
                {
                    break;
                }
            }
        }

        void print(const DataMatrixT& data, int n = 10) const
        {
            int numrows = 0;
            for (auto row: data)
            {
                numrows++;
                for (auto col: row)
                {
                    std::cout << std::setw(_spacing) << col << " ";
                }
                std::cout << std::endl;
                if ((n != -1) && (numrows == n))
                {
                    break;
                }
            }
        }

        void print(const DataVectorT& data, int n = 10) const
        {
            int numrows = 0;
            for (auto row: data)
            {
                numrows++;
                std::cout << std::setw(_spacing) << row << std::endl;
                if ((n != -1) && (numrows == n))
                {
                    break;
                }
            }
        }

        bool read(int ycol = -1, const std::string& delimiter=",", int header=-1)
        {
            std::string line;

            int row = 0;
            int col = 0;
            int lineno = 0;

            _DEBUG_("read", "START");
            // std::string delim_pattern = "\\s*" + std::string(delimiter);
            std::string delim_pattern = delimiter;
            _DEBUG_("read delim", delim_pattern);

            while(getline(fp, line))
            {
                // std::regex reg("\\s*,");
                std::regex reg(delim_pattern);
                std::sregex_token_iterator iter(line.begin(), line.end(), reg, -1);
                std::sregex_token_iterator end;

                std::vector<std::string> vec(iter, end);
                for (auto v: vec)
                {
                    _DEBUG_("read value: ", v);
                }


                // Later store the header as column names
                std::string debug_header;

                if (lineno < header)
                {
                    continue;
                }
                else if (lineno == header)
                {
                    
                    int index = 0;
                    for (auto v: vec)
                    {
                        if (v == "")
                        {
                            continue;
                        }
                        if ((v[v.length() -1] == '\n') || (v[v.length() -1] == '\r'))
                        {
                            v.erase(v.length() -1);
                        }
                        col_names_to_index.insert(std::pair<std::string, int>(v, index));
                        col_names_vector.push_back(v);
                        debug_header += v;
                        debug_header += " ";
                        index++;
                        _DEBUG_("column: ", v);
                    }
                    lineno++;
                    _DEBUG_("column names", debug_header);
                    continue;
                }
                std::stringstream line_debug;
                line_debug << "LINE: " << lineno;
                _DEBUG_("read", line_debug.str());
                lineno++;
                
                DataVectorT row_vec;
                DataVectorT y_row_vec;
                col = 0;
                for (auto v: vec)
                {
                    if (v == "")
                    {
                        continue;
                    }
                    // _DEBUG_("read", v);
                    double n = stof(v);
                    if ((ycol != -1) && (ycol == col))
                    {
                        y_row_vec.push_back(n);
                    }
                    else
                    {
                        row_vec.push_back(n);
                    
                        if (row == 0)
                        {
                            std::vector<double> col_vec;
                            data_transpose.push_back(col_vec);
                        }
                        data_transpose[col].push_back(n);
                        col++;
                    }
                }
                row++;
                data.push_back(row_vec);
                Y.push_back(y_row_vec);
            }
            calculate_column_stats();
            // std::cout << "shape of data: (" << row << "," << col << ")" << std::endl;
            // std::cout << "shape of data from vector: (" << data.size() << "," << data[0].size() << ")" << std::endl;
            // std::cout << "shape of transposed data: (" << data_transpose.size() << "," << data_transpose[0].size() << ")" << std::endl;
            _DEBUG_("read", "END");
            return true;
        }

        const DataMatrixT& transpose() const
        {
            return data_transpose;
        }

        void describe()
        {
            int col_num = 0;

            std::cout << std::endl;
            // Print a header
            if (col_names_vector.size() > 0)
            {
                std::cout << std::setw(_spacing) << "NAME:";
            }
            std::cout << std::setw(_spacing) << "MEAN"; 
            std::cout << std::setw(_spacing) << "STD";
            std::cout << std::setw(_spacing) << "MIN";
            std::cout << std::setw(_spacing) << "MAX"; 
            std::cout << std::setw(_spacing) << "SUM";
            std::cout << std::setw(_spacing) << "Q1";
            std::cout << std::setw(_spacing) << "Q2";
            std::cout << std::setw(_spacing) << "Q3";
            std::cout << std::endl;

            // Print the statistics
            for (auto s: col_stats)
            {
                if (col_names_vector.size() > 0)
                {
                    std::cout << std::setw(_spacing) << col_names_vector[col_num] << ":";
                }
                std::cout << std::setw(_spacing) << col_stats[col_num].mean;
                std::cout << std::setw(_spacing) << col_stats[col_num].std;
                std::cout << std::setw(_spacing) << col_stats[col_num].min;
                std::cout << std::setw(_spacing) << col_stats[col_num].max;
                std::cout << std::setw(_spacing) << col_stats[col_num].sum;
                std::cout << std::setw(_spacing) << col_stats[col_num].q1;
                std::cout << std::setw(_spacing) << col_stats[col_num].q2;
                std::cout << std::setw(_spacing) << col_stats[col_num].q3;
                std::cout << std::endl;
                col_num++;
            }
        }

        std::tuple<int, int> shape(const DataMatrixT& data)
        {
            int l = data.size(); 
            int w = (l > 0) ? data[0].size(): 0;
            return std::make_tuple(l, w);
        }

        const DataMatrixT onehot(const DataMatrixT& y) const
        {
            std::set<double> set;
            for (auto row: y)
            {
                for (auto col: row)
                {
                    set.insert(col);
                }
            }
            int size = set.size();
            std::cout << "One hot: no. of unique values = " << size << std::endl;
            std::vector<double> unique_values(set.begin(), set.end());

            DataMatrixT return_y;
            
            for (auto row: y)
            {
                std::vector<double> row_vec;
                for (auto col: row)
                {
                    std::vector<double>::iterator it = std::find(unique_values.begin(), unique_values.end(), col);
                    int index = std::distance(unique_values.begin(), it);
                    for (int i = size-1; i >= 0; i--)
                    {
                        row_vec.push_back((i==index) ? 1.0 : 0.0);
                    }
                    
                }
                return_y.push_back(row_vec);
            }
            return return_y;
        }

        void onehot_y()
        {
            auto y_ret = onehot(Y);
            Y.clear();
            Y = y_ret;
        }

        const DataVectorT min_max_scaler(const DataVectorT& column) const
        {
            double max = -0xFFFFFFFF;
            double min = 0xffffffff;
            DataVectorT scaled;

            for (auto v: column)
            {
                if (v > max)
                {
                    max = v;
                }
                if (v < min)
                {
                    min = v;
                }
            }
            for (int i = 0; i < column.size(); i++)
            {
                scaled.push_back((column[i] - min) / (max - min));
            }
            return scaled;
        }

        const DataVectorT standard_scaler(const DataVectorT& column) const
        {
            double mean = 0.0;
            double sum = 0.0;
            double std = 0.0;
            DataVectorT scaled;

            for (auto v: column)
            {
                sum += v; 
            }
            mean = sum / column.size(); 

            for (auto v: column)
            {
                std += pow((v - mean), 2.0);
            }
            std = sqrt(std/(column.size() - 1));

            for (auto v : column)
            {
                scaled.push_back((v - mean)/std);
            }
            return scaled;
        }

        const DataMatrixT normalize(const DataMatrixT& data) const
        {
            DataMatrixT  col_matrix;
            DataMatrixT returned;

            for (auto row: data)
            {
                for (auto col: row)
                {
                    DataVectorT col_vec;
                    col_matrix.push_back(col_vec);
                }
                break;
            }

            int col_index = 0;
            for (auto row: data)
            {
                col_index = 0;
                for (auto col: row)
                {
                    col_matrix[col_index].push_back(col);
                    col_index++;
                }
                std::vector<double> row_vec;
                returned.push_back(row_vec);
            }
            // std::cout << "Printing column matrix of X" << std::endl;
            // print(col_matrix, 10);

            col_index = 0;
            for (auto column: col_matrix)
            {
                auto scaled = standard_scaler(column);
                int row_index = 0;
                for (auto col: scaled)
                {
                    returned[row_index].push_back(col);
                    row_index++;
                }
                col_index++;
            }
            return returned;
        }
        
        std::tuple<DataMatrixT, DataMatrixT, DataMatrixT, DataMatrixT> train_test_split(float test_ratio=0.30) const
        {
            int train_bound = floor(data.size() * (1-test_ratio));
            std::tuple<DataMatrixT, DataMatrixT, DataMatrixT, DataMatrixT> returned_data;
            DataMatrixT X_train, Y_train, X_test, Y_test;
            std::set<int> index_set;
            for (int i = 0; i < train_bound; i++)
            {
                int index = rand() % data.size();
                X_train.push_back(data[index]);
                Y_train.push_back(Y[index]);
                index_set.insert(index);
            }
            int test_size = data.size() - train_bound;
            do
            {
                int index = rand() % data.size();
                auto itr = index_set.find(index);
                if (itr == index_set.end())
                {
                    X_test.push_back(data[index]);
                    Y_test.push_back(Y[index]);
                    test_size--;
                }
            } while(test_size > 0);
            returned_data = std::make_tuple(X_train, Y_train, X_test, Y_test);
            return returned_data;
        }
};
