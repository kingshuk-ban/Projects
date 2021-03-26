#include <iostream>
#include <vector>
#include <functional>
#include <math.h>


double sigmoid(const std::vector<double>& inputs, const std::vector<double>& wts)
{
    //std::cout << "Applying sigmoid on " << wts.size() << " inputs " << std::endl;
    double z = wts[0];
    for (int i = 1; i < wts.size(); i++)
    {
        z += wts[i] * inputs[i-1];
    }
    return (1.0/(1.0 + exp(-z)));
}

double sigmoid_derivative(double output)
{
    return output * (1.0 - output);
}

double relu(const std::vector<double>& inputs, const std::vector<double>& wts)
{
    //std::cout << "Applying relu on " << wts.size() << " inputs " << std::endl;
    double z = wts[0];
    for (int i = 1; i < wts.size(); i++)
    {
        z += wts[i] * inputs[i-1];
    }
    return fmax(0.0, z);
}

double relu_derivative(double output)
{
    return (output <= 0.0) ? 0.0 : 1.0;
}

double init_weight()
{
    // srand(10);
    // double w = rand() % 10;
    // return w/100.0; 
    return 0.05;
}

class neuron {
    private:
        int num_inputs;
        double output_;
        double delta;
        std::vector<double> weights;
        std::function<double(const std::vector<double>&, const std::vector<double>&)> activation = sigmoid;
        std::function<double(void)> initialize_weights = init_weight;
        std::function<double(double)> derivative = sigmoid_derivative;
        int neuronId; 
        static int count;

        //neuron(const neuron&);
        neuron& operator=(const neuron&);

    public:
        neuron(int n_inputs, const std::vector<double>& init_wts)
        {
            num_inputs = n_inputs;
            for (int i = 0; i < init_wts.size(); i++)
                weights.push_back(init_wts[i]);
            for (int i = init_wts.size(); i < n_inputs+1; i++)
                weights.push_back(init_wts[i-init_wts.size()]);
            if (weights.size() != n_inputs+1)
            {
                std::cerr << "No. of weights " << init_wts.size() << " does not match no. of inputs " << n_inputs << std::endl;
            }
            neuronId = neuron::count++;
            output_ = -1; 
            delta = -1;
            std::cout << "Neuron: " << neuronId << " created." << std::endl;
        }
        neuron(int n_inputs)
        {
            num_inputs = n_inputs;
            for (int i = 0; i < n_inputs+1; i++)
            {
                weights.push_back(initialize_weights());
            }
            neuronId = neuron::count++;
            output_ = -1;
            delta = -1;
            std::cout << "Neuron: " << neuronId << " created." << std::endl;
        }
        ~neuron()
        {
        }

        void set_activation_fn(std::function<double(const std::vector<double>&, const std::vector<double>&)> act_fn, std::function<double(double)> derivative_fn)
        {
            activation = act_fn;
        }

        void set_initialize_wts_fn(std::function<double(void)> init_wt_fn)
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

        double getOutput() const 
        {
            return output_;
        }

        void calculate_error(double expected)
        {
            double error = expected - output_;
            // std::cout << "Neuron : " << neuronId << " Error: " << error << " Exp: " << expected << " output " << output_ << std::endl;
            delta = error * derivative(output_);
            // std::cout << "Neuron : " << neuronId << " delta: " << delta << std::endl;
        }

        void calculate_error(int self_index, const std::vector<neuron>& f_neurons)
        {
            double error = 0.0;
            for (int i = 0; i < f_neurons.size(); i++)
            {
                const neuron& f_neuron = f_neurons[i];
                error += f_neuron.weight(self_index) * f_neuron.getdelta();
            }
            delta = error * derivative(output_);
            // std::cout << "Neuron : " << neuronId << " delta_: " << delta << std::endl;
        }

        void update_weights(const std::vector<double>& inputs, double l_rate)
        {
            weights[0] += l_rate * delta; 
            for (int i = 1; i < weights.size(); i++)
            {
                weights[i] += l_rate * delta * inputs[i-1];
            }
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
        Layer(int n_inputs, int n_neurons, const std::vector<double>& init_wts)
        {
            num_inputs = n_inputs;
            for (int i = 0; i < n_neurons; i++)
            {
                neurons.push_back(neuron(n_inputs, init_wts));
            }
            layerId = Layer::count++;
            std::cout << Layer::layerId << ": Initialized a layer of " << n_neurons << " neurons with " << n_inputs << " inputs." << std::endl;
        }
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

        void calculate_error(const std::vector<double>& outputs)
        {
            // std::cout << "Calculating error in final layer: " << layerId << std::endl;
            for (int i = 0; i < neurons.size(); i++)
            {
                // std::cout << "Neuron : " << neurons[i].getId() << " output_ : " << neurons[i].getOutput() << std::endl;
                neurons[i].calculate_error(outputs[i]);
            }
        }

        void calculate_error(const Layer& successor)
        {
            // std::cout << "Calculating error in middle layer: " << layerId << std::endl;
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

    public:
        Network() {}
        ~Network() 
        {
            layers.clear();
        }
        void addInput(int n_inputs, int n_neurons, const std::vector<double>& init_wts)
        {
            layers.push_back(Layer(n_inputs, n_neurons, init_wts));
        }
        void addHidden(int n_neurons, const std::vector<double>& init_wts)
        {
            layers.push_back(Layer(layers.back().num_neurons(), n_neurons, init_wts));
        }
        void addOutput(int n_outputs, const std::vector<double>& init_wts)
        {
            layers.push_back(Layer(layers.back().num_neurons(), n_outputs, init_wts));
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
            const std::vector<double>& output = ip.output();
            for (int i = 1; i < layers.size(); i++)
            {
                Layer& hidden = layers[i];
                hidden.feed_forward(output);
                const std::vector<double>& output = hidden.output();
            }
            // layers.back().printOutput();
            outputs = layers.back().output();
        }

        void backward_propagate(const std::vector<double>& outputs)
        {
            Layer& lp = layers.back();
            lp.calculate_error(outputs);
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
            const std::vector<double>& output = ip.output();
            for (int i = 1; i < layers.size(); i++)
            {
                Layer& hidden = layers[i];
                hidden.update_weights(output, l_rate);
                const std::vector<double>& output = hidden.output();
            }
        }

        const std::vector<double>& output() const
        {
            const std::vector<double>& o = layers.back().output();
            layers.back().printOutput();
            return o;
        }

        void train(double l_rate, int num_epochs, const std::vector<std::vector<double> >& X, const std::vector<std::vector<double> >& Y)
        {
            int least_epoch = 0;
            double least_error = 100.0;
            for (int e = 0; e < num_epochs; e++)
            {
                double sum_error = 0.0;
                for (int i = 0; i < X.size(); i++)
                {
                    forward_propagate(X[i]);
                    backward_propagate(Y[i]);
                    update_weights(X[i], l_rate);
                    for (int j = 0; j < outputs.size(); j++)
                        sum_error += pow((Y[i][j] - outputs[j]), 2.0);
                }
                std::cout << "Epoch: " << e << " l_rate: " << l_rate << " sum_error: " << sum_error << std::endl;
                if (sum_error < least_error)
                {
                    least_error = sum_error;
                    least_epoch = e;
                }
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

int main()
{
    /*
    double arr[] = {1.1, 2.2, 3.3, 4.4, 5.5};
    std::vector<double> X (arr, arr + sizeof(arr)/sizeof(double));
    double y = 1.0;
    std::vector<double> Y;
    Y.push_back(y);
    */

    std::vector<std::vector<double> > X {
        {2.7810836,2.550537003},
	    {1.465489372,2.362125076},
	    {3.396561688,4.400293529},
	    {1.38807019,1.850220317},
	    {3.06407232,3.005305973},
	    {7.627531214,2.759262235},
	    {5.332441248,2.088626775},
	    {6.922596716,1.77106367},
	    {8.675418651,-0.242068655},
	    {7.673756466,3.508563011}
    };

    std::vector<std::vector<double> > Y {
        {1.0, 0.0},
        {1.0, 0.0},
        {0.0, 1.0},
        {1.0, 0.0},
        {0.0, 1.0},
        {0.0, 1.0},
        {0.0, 1.0},
        {1.0, 0.0},
        {1.0, 0.0},
        {0.0, 1.0}
    };

    Network network;
    network.addInput(2, 2, sigmoid, sigmoid_derivative);
    //network.addHidden(10, sigmoid, sigmoid_derivative);
    network.addHidden(5, sigmoid, sigmoid_derivative);
    network.addOutput(2, sigmoid, sigmoid_derivative);

    network.train(0.5, 2000, X, Y);
    std::vector<std::vector<double> > preds;
    network.predict(X, preds);
    double accuracy=network.compare(Y, preds);
    std::cout << "Accuracy: " << accuracy << std::endl; 
    
}
