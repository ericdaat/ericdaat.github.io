Title: Single Layer Neural Network
Date: 2010-12-03 10:20
Modified: 2010-12-03 10:20
Category: Data Science
Tags: python, machine-learning, neural-networks
Slug: single-layer-neural-network
Authors: Eric Daoud
Summary: In this post we are going to introduce Single Layer Neural Networks and understand how they work by implementing one from scratch in Python (without using Deep Learning Frameworks such as TensorFlow or Keras).
Status: draft


Neural Networks are a really hot topic right now and are used in so many applications, from face recognition to Natural Language Processing. The core concept of Neural Networks is however quite old and many large discoveries have been made during the 70s. At the time, computers weren't efficient enough to run large computations, and not a lot of data were available to feed the networks. Recently, with the "Big Data" era and the progress made in computing, we can train very large Neural Networks on huge amounts of data to solve complex problems. It is a new way of programming based on a simplified version of how a brain works. Very simplified actually, I heard that the State of the Art deep Neural Networks used by giant tech companies are solely comparable to worm's brain, and yet they can perform some quite amazing tasks !

In this post we are going to introduce Single Layer Neural Networks and understand how they work by implementing one from scratch in Python (without using Deep Learning Frameworks such as TensorFlow or Keras).

## About neural networks

Neural networks are a succession of layers composed by nodes (similar to neurons). All the nodes from each layer are fully connected to the nodes from the surrounding layers by connections (similar to synapses). The neurons and connections hold float values that change when the network is training:

 - The values hold by connections are called weights. The set of weights between two fully connected layers forms a matrix that we call $W$
 - The values hold by neurons are usually obtained by a transformation that involves the weights previously defined.

 A very simplified Neural Network could look like this:


### Layers
A single hidden layer neural network has 3 different layers:

- An input layer $X$ of size $P$
- A hidden layer $Z$ of size $M$
- An output layer $Y$ of size $K$

<img src="/images/neural-net.png" width=400px/>

Each layer is computed from the layer below using weights and an activation function.

The hidden layer is computed by $Z_m = \sigma (\alpha_{0m} + \alpha_{m}^{T} X)$; with $m = 1, \ldots, M$ and the output layer with $Y_k = g_k(\beta_{0k} + \beta_{k}^{T} Z)$; with $k = 1, \ldots, K$.

The two matrices $\alpha$ and $\beta$ contain the parameters of the model, composed by weights and biases. For instance, the $\alpha$ matrix contains both biases and weights between the input and the hidden layer.

\begin{equation}
    \alpha = \begin{pmatrix}
        \alpha_{00} & \alpha_{01} & \ldots & \alpha_{0M} \\
        \vdots & \vdots & \ldots & \vdots \\
        \alpha_{P0} & \alpha_{P1} & \ldots & \alpha_{PM} \\
    \end{pmatrix}
\end{equation}

\begin{equation}
    b_\alpha = \begin{pmatrix}
        \alpha_{00} \\
        \vdots \\
        \alpha_{P0} \\
    \end{pmatrix}
\end{equation}

\begin{equation}
    W_\alpha = \begin{pmatrix}
        \alpha_{01} & \ldots & \alpha_{0M} \\
        \vdots & \ldots & \vdots \\
        \alpha_{P1} & \ldots & \alpha_{PM} \\
    \end{pmatrix}
\end{equation}

To compute the hidden layer neurons, we use a non linear function $\sigma$ which is typically a sigmoid or tanh function. Regarding the output layer neurons, there are two cases:
 - For a regression problem, $K=1$ and we use the identity function
 - For a $K$ class classifiction problem, we often use a softmax function $g_k(T) = \frac{e^{T_k}}{\sum_{l=1}{K}e^{T_l}}$. The softmax function outputs probabilities of each class corresponding to our input. We simply use $argmax_k(g_k(T))$ as our classifier to keep the class with the largest probability.

### Training the network

Let's call $\theta$ the set of weights $\alpha$ and $\beta$: $\theta = (\{\alpha_{0m}, \alpha_{m}; m=1, \ldots M\}, \{\beta_{0k}, \beta_{k}; k=1, \ldots K\})$

Training is achieved by minimizing a loss function $R(\theta)$ that we define depending on the task we want to achieve:
- For regression, we use sum of squared error:
\begin{equation}
    R(\theta) = \sum_{k=1}^{K} \sum_{i=1}^{N} (y_{ik} - f_k(x_i))^2
\end{equation}
- For classification, we use cros entropy:
\begin{equation}
    R(\theta) = - \sum_{i=1}^{N} \sum_{k=1}^{K} y_{ik} log(f_k(x_i))
\end{equation}

We minimize the loss function using gradient descent

## Sources
 [0] [The Elements of Statistical Learning](#)
 [1] [Implementing a Neural Network from scratch](http://www.wildml.com/2015/09/implementing-a-neural-network-from-scratch/)

## Code


```python
from sklearn.datasets import make_moons
import numpy as np
import logging
from matplotlib import pyplot as plt
plt.style.use('ggplot')

np.random.seed(0)
X, y = make_moons(200, noise=0.2)
y_onehot = np.zeros((200, 2))
y_onehot[np.arange(200), y] = 1
```


```python
%matplotlib inline

plt.scatter(X[:,0],
            X[:,1],
            color=['r' if item == 1 else 'b' for item in y]
)
```

![png](/images/slnn-moons.png)


## Implementation from scratch


```python
class SingleLayerNeuralNetwork():
    def __init__(self, input_layer_size, hidden_layer_size, output_layer_size,
                 learning_rate, regularization_rate):
        # neural network parameters
        self._input_layer_size = input_layer_size
        self._hidden_layer_size = hidden_layer_size
        self._output_layer_size = output_layer_size
        self._learning_rate = learning_rate
        self._regularization_rate = regularization_rate


        # parameters random initilization
        np.random.seed(0)
        self._W_h = np.random.randn(self._input_layer_size, self._hidden_layer_size) \
                        / np.sqrt(self._input_layer_size)
        self._b_h = np.zeros((1, self._hidden_layer_size))
        self._W_o = np.random.randn(self._hidden_layer_size, self._output_layer_size) \
                        / np.sqrt(self._output_layer_size)
        self._b_o = np.zeros((1, self._output_layer_size))

    def _softmax(self, X):
        """ Takes an input matrix X, returns an array of probabilities.
        This function takes the input layer X through the entire network
        and returns the softmax function result, corresponding to the
        output layer.
        """

        z_h = X.dot(self._W_h) + self._b_h
        h_1 = np.tanh(z_h)
        z_o = h_1.dot(self._W_o) + self._b_o
        softmax = np.exp(z_o) / np.sum(np.exp(z_o), axis=1, keepdims=True)

        return softmax

    def _calculate_loss(self, X, y):
        """ Takes an input matrix X and one hot encoded output values y,
        returns the loss function result.
        """
        softmax = self._softmax(X)

        return -np.sum(np.multiply(y, np.log(softmax)))

    def predict(self, X):
        """ Takes an input matrix X, returns the predicted class
        according to the argmax over the softmax function result.
        """
        softmax = self._softmax(X)

        return np.argmax(softmax, axis=1)

    def train(self, X, y, epochs):
        """ Takes an input matrix X, one hot encoded output matrix y
        and number ofepochs. Trains the network with gradient descent and
        returns an array of loss function results.
        """
        losses = []
        for i in range(epochs):
            # forward propagation
            z_h = X.dot(self._W_h) + self._b_h
            h_1 = np.tanh(z_h)
            z_o = h_1.dot(self._W_o) + self._b_o
            exp_z_o = np.exp(z_o)
            softmax = exp_z_o / np.sum(exp_z_o, axis=1, keepdims=True)

            # compute loss for debug
            if i % 10 == 0:
                loss = self._calculate_loss(X, y)
                losses.append(loss)
                logging.debug("loss after {0}-th iteration: {1}".format(i, loss))

            # back propagation
            ## computing output layer weight updates
            delta_o = softmax - y
            dW_o = h_1.T.dot(delta_o)
            db_o = np.sum(delta_o, axis=0, keepdims=True)
            ## computing hidden layer weight updates
            delta_h = delta_o.dot(self._W_o.T) * (1 - np.power(h_1, 2))
            dW_h = np.dot(X.T, delta_h)
            db_h = np.sum(delta_h, axis=0)

            ## applying regularization
            dW_h += self._regularization_rate * self._W_h
            dW_o += self._regularization_rate * self._W_o

            ## parameters update controled by learning rate
            self._W_h += -self._learning_rate * dW_h
            self._b_h += -self._learning_rate * db_h
            self._W_o += -self._learning_rate * dW_o
            self._b_o += -self._learning_rate * db_o

        return losses
```


```python
%matplotlib inline

slnn = SingleLayerNeuralNetwork(
        input_layer_size = 2,
        hidden_layer_size = 4,
        output_layer_size = 2,
        learning_rate = 0.01,
        regularization_rate = 0.1
)

%time losses = slnn.train(X, y_onehot, 1000)
accuracy = (len(X) - float(np.sum(np.power((slnn.predict(X) - y), 2)))) / len(X)
logging.info(accuracy)
plt.plot(losses)
```

    CPU times: user 217 ms, sys: 2.91 ms, total: 220 ms
    Wall time: 220 ms


![png](/images/slnn-loss.png)

