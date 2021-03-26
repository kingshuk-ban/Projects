#pragma once

#include <iostream>
#include <vector>
#include <functional>
#include <math.h>
#include "common.h"

class neuron {
    private:
        int num_inputs;
        double output_;
        double delta;
        double error;
        std::vector<double> weights;
        std::function<double(const std::vector<double>&, const std::vector<double>&)> activation = sigmoid;
        std::function<double(int)> initialize_weights = init_weight;
        std::function<double(double)> derivative = sigmoid_derivative;
        int neuronId; 
        static int count;
        int batch_size; 

        //neuron(const neuron&);
        neuron& operator=(const neuron&);

    public:
        neuron(int n_inputs)
        {
            num_inputs = n_inputs;
            for (int i = 0; i < n_inputs+1; i++)
            {
                weights.push_back(initialize_weights(n_inputs));
            }
            neuronId = neuron::count++;
            output_ = -1;
            delta = -1;
            batch_size = 0;
            std::cout << "Neuron: " << neuronId << " created with " << n_inputs << " inputs." << std::endl;
        }
        ~neuron()
        {
        }

        void set_activation_fn(std::function<double(const std::vector<double>&, const std::vector<double>&)> act_fn, std::function<double(double)> derivative_fn)
        {
            activation = act_fn;
        }

        void set_initialize_wts_fn(std::function<double(int)> init_wt_fn)
        {
            initialize_weights = init_wt_fn;
        }

        double activate(const std::vector<double>& inputs)
        {
            output_ = activation(inputs, weights);
            // std::cout << "Neuron : " << neuronId << " activated. Output = " << output_ << std::endl;
            return output_;
        }

        int getId() const { return neuronId; }
    
        double weight(int index) const
        {
            return weights[index];
        }

        double getdelta() const 
        {
            return delta;
        }

        double geterror() const
        {
            return error;
        }

        double getOutput() const 
        {
            return output_;
        }

        void calculate_error(double expected)
        {
            double error = expected - output_;
            // std::cout << "Neuron : " << neuronId << " Error: " << error << " Exp: " << expected << " output " << output_ << std::endl;
            delta += error * derivative(output_);
            // std::cout << "Neuron : " << neuronId << " delta: " << delta << std::endl;
            batch_size++;
        }

        void calculate_error(int self_index, const std::vector<neuron>& f_neurons)
        {
            error = 0.0;
            // std::cout << "Error calculation for neuron: " << neuronId << std::endl;
            for (int i = 0; i < f_neurons.size(); i++)
            {
                const neuron& f_neuron = f_neurons[i];
                error += f_neuron.weight(self_index) * f_neuron.getdelta();
                // error += f_neuron.weight(self_index) * f_neuron.geterror();
                // std::cout << "      successor neuron: " << f_neuron.getId() << " wt = " << f_neuron.weight(self_index) << " delta = " << f_neuron.getdelta() << std::endl;
             }
            delta += error * derivative(output_);
            // std::cout << "Neuron : " << neuronId << " error: " << error << " delta_: " << delta << std::endl;
            batch_size++;
        }

        void update_weights(const std::vector<double>& inputs, double l_rate)
        {
            // assert(inputs.size() == num_inputs);
            // assert(weights.size() == num_inputs+1);
            if (inputs.size() != num_inputs)
            {
                std::cerr << "Invalid input size passed to neuron : " << neuronId << " n_inputs: " 
                        << num_inputs << " passed: " << inputs.size() << std::endl;
                std::terminate();
            }
            delta = delta / batch_size;
            for (int i = 0; i < inputs.size(); i++)
            {
                weights[i] += l_rate * delta * inputs[i];
            }
            weights[weights.size() - 1] += l_rate * delta;
            batch_size = 0;
            delta = 0.0;
        }

        void print_weights() const 
        {
            std::cout << "Neuron " << neuronId << " weights: { ";
            for (int i = 0; i < weights.size(); i++)
            {
                std::cout << weights[i] << " ";
            }
            std::cout << "} ";
            std::cout << "output: " << output_ << " delta: " << delta << std::endl;

        }
};

int neuron::count = 0;

class Layer {
    private:
        int num_inputs;
        std::vector<neuron> neurons;
        std::vector<double> outputs;
        std::vector<double> errors;
        int layerId;
        static int count;

    public:
        Layer(int n_inputs, int n_neurons)
        {
            num_inputs = n_inputs;
            for (int i = 0; i < n_neurons; i++)
            {
                neurons.push_back(neuron(n_inputs));
            }
            layerId = Layer::count++;
            std::cout << Layer::layerId << ": Initiliazed a layer of " << n_neurons << " neurons with " << n_inputs << " inputs." << std::endl;
            
        }
        Layer(int n_inputs, int n_neurons, 
                std::function<double(const std::vector<double>&, const std::vector<double>&)> act_fn,
                std::function<double(double)> derivative_fn)
        {
            num_inputs = n_inputs;
            for (int i = 0; i < n_neurons; i++)
            {
                neurons.push_back(neuron(n_inputs));
                neurons.back().set_activation_fn(act_fn, derivative_fn);
            }
            layerId = Layer::count++;
            std::cout << Layer::layerId << ": Initiliazed a layer of " << n_neurons << " neurons with " << n_inputs << " inputs." << std::endl;
        }
        ~Layer()
        {
            neurons.clear();
        }

        int getLayerId() const 
        {
            return layerId;
        }

        void feed_forward(const std::vector<double>& inputs)
        {
            // std::cout << "Feed forward: " << layerId << std::endl;
            outputs.clear();
            for (int i = 0; i < neurons.size(); i++)
            {
                double out = neurons[i].activate(inputs);
                outputs.push_back(out);
            }
        }

        void calculate_error(const std::vector<double>& expected)
        {
            // std::cout << "Calculating error in final layer: " << layerId << std::endl;
            
            for (int i = 0; i < neurons.size(); i++)
            {
                // std::cout << "Neuron : " << neurons[i].getId() << " output_ : " << neurons[i].getOutput() << std::endl;
                neurons[i].calculate_error(expected[i]);
                // std::cout << neurons[i].getOutput() << " (" << expected[i] << ") ";
            }
            // std::cout << std::endl;
        }

        void calculate_error(const Layer& successor)
        {
            // std::cout << "Calculating error in middle layer: " << layerId << " sucessor layer: " << successor.getLayerId() << std::endl;
            for (int i = 0; i < neurons.size(); i++)
            {
                neurons[i].calculate_error(i, successor.get_neurons());
            }
        }

        void update_weights(const std::vector<double>& inputs, double l_rate)
        {
            // std::cout << "Updating weights: " << layerId << std::endl;
            for (int i = 0; i < neurons.size(); i++)
            {
                neurons[i].update_weights(inputs, l_rate);
            }
        }

        const std::vector<double>& output() const
        {
            return outputs;
        }

        int num_neurons() const { return neurons.size(); }

        const std::vector<neuron>& get_neurons() const
        {
            return neurons;
        }

        const neuron& get_neuron(int index) const
        {
            return neurons[index];
        }

        void printOutput() const
        {
            for (int i = 0; i < outputs.size(); i++)
            {
                std::cout << outputs[i] << " ";
            }
            std::cout << std::endl;
        }

        void print_weights() const
        {
            for (int i = 0; i < neurons.size(); i++)
            {
                neurons[i].print_weights();
            }
        }
};

int Layer::count = 0;

static int decodeClass(const std::vector<double>& outputs)
{
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

class Network {
    private:
        std::vector<Layer> layers;
        int num_layers;
        std::vector<double> outputs;
        double seed;

    public:
        Network(double seed = 1.0) 
        {
            srand(seed);
        }
        ~Network() 
        {
            layers.clear();
        }
        void addInput(int n_inputs, int n_neurons)
        {
            layers.push_back(Layer(n_inputs, n_neurons));
        }
        void addHidden(int n_neurons)
        {
            layers.push_back(Layer(layers.back().num_neurons(), n_neurons));
        }
        void addOutput(int n_outputs)
        {
            layers.push_back(Layer(layers.back().num_neurons(), n_outputs));
        }
        void addInput(int n_inputs, int n_neurons, 
            std::function<double(const std::vector<double>&, const std::vector<double>&)> act_fn,
            std::function<double(double)> derivative_fn)
        {
            layers.push_back(Layer(n_inputs, n_neurons, act_fn, derivative_fn));
        }
        void addHidden(int n_neurons, 
            std::function<double(const std::vector<double>&, const std::vector<double>&)> act_fn,
            std::function<double(double)> derivative_fn)
        {
            layers.push_back(Layer(layers.back().num_neurons(), n_neurons, act_fn, derivative_fn));
        }
        void addOutput(int n_outputs, 
            std::function<double(const std::vector<double>&, const std::vector<double>&)> act_fn,
            std::function<double(double)> derivative_fn)
        {
            layers.push_back(Layer(layers.back().num_neurons(), n_outputs, act_fn, derivative_fn));
        }

        void forward_propagate(const std::vector<double>& inputs)
        {
            Layer& ip = layers[0];
            ip.feed_forward(inputs);
            std::vector<double> output_ = ip.output();
            for (int i = 1; i < layers.size(); i++)
            {
                Layer& hidden = layers[i];
                hidden.feed_forward(output_);
                output_ = hidden.output();
            }
            // layers.back().printOutput();
            outputs = layers.back().output();
        }

        void backward_propagate(const std::vector<double>& expected)
        {
            Layer& lp = layers.back();
            lp.calculate_error(expected);
            for (int i = layers.size() - 2; i >= 0; i--)
            {
                Layer& back_l = layers[i];
                back_l.calculate_error(layers[i+1]);
                //lp = back_l;
            }
        }

        void update_weights(const std::vector<double>& inputs, double l_rate)
        {
            Layer& ip = layers[0];
            ip.update_weights(inputs, l_rate);
            std::vector<double> output_ = ip.output();
            for (int i = 1; i < layers.size(); i++)
            {
                Layer& hidden = layers[i];
                hidden.update_weights(output_, l_rate);
                output_ = hidden.output();
            }
        }

        const std::vector<double>& output() const
        {
            const std::vector<double>& o = layers.back().output();
            // layers.back().printOutput();
            return o;
        }

        void print_weights() const
        {
            for (int i = 0; i < layers.size(); i++)
            {
                layers[i].print_weights();
            }
        }

        void train(double l_rate, int num_epochs, const std::vector<std::vector<double> >& X, const std::vector<std::vector<double> >& Y)
        {
            int least_epoch = 0;
            double least_error = 100.0;
            std::vector<std::vector<double> > preds; // for debug

            for (int e = 0; e < num_epochs; e++)
            {
                double sum_error = 0.0;
                for (int i = 0; i < X.size(); i++)
                {
                    forward_propagate(X[i]);
                    backward_propagate(Y[i]);
                    // int y = decodeClass(Y[i]); // for debug
                    // int p = decodeClass(outputs); // for debug
                    // std::cout << "  X[" << i << "] Y = " << y << " P = " << p << std::endl; // for debug

                    // if ((i % 50) == 0) {
                        update_weights(X[i], l_rate);
                    // }
                    
                    for (int j = 0; j < outputs.size(); j++)
                        sum_error += pow((Y[i][j] - outputs[j]), 2.0);
                    // print_weights(); // for debug
                }
                // update_weights(X[0], l_rate);
                std::cout << "Epoch: " << e << "/" << num_epochs << " loss: " << sum_error << std::endl;
                if (sum_error < least_error)
                {
                    least_error = sum_error;
                    least_epoch = e;
                }
                // print_weights(); // for debug
                // preds.clear(); // for debug
                // predict(X, preds); // for debug
                // double score = compare(Y, preds); // for debug
                // std::cout << "Accuracy at end of epoch " << e << " : " << score << std::endl; // for debug
             }
             std::cout << "The least error " << least_error << " was achieved in " << least_epoch << "." << std::endl;
        }

        void predict(const std::vector<std::vector<double> >& X, std::vector<std::vector<double> >& predictions)
        {
            for (int i = 0; i < X.size(); i++)
            {
                forward_propagate(X[i]);
                // layers.back().printOutput();
                predictions.push_back(outputs);
                // int p = decodeClass(outputs); // for debug
                // std::cout << "  Prediction cycle: X[" << i << "] P = " << p << std::endl; // for debug
            }
        }

        double compare(const std::vector<std::vector<double> >& Y, const std::vector<std::vector<double> >& predictions)
        {
            double score = 0.0;
            for (int i = 0; i < Y.size(); i++)
            {
                int y = decodeClass(Y[i]);
                int p = decodeClass(predictions[i]);
                std::cout << "Expected: " << y << " Actual: " << p << std::endl;
                if (y == p) 
                {
                    score = score + 1.0;
                }
            }
            return (score/Y.size()) * 100.0;
        }

};

