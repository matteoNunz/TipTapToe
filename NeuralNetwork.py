"""
Date: 21/10/2021
Author: Matteo Nunziante

Description: Neural Network -> first sketch with keras library
"""

# To load the dataSet
from numpy import loadtxt
# To define the model
from keras.models import Sequential
from keras.layers import Dense


# Load the data set (9 columns)
dataSet = loadtxt('Files/Pima-Indians-Diabetes.csv' , delimiter = ',')
# Split into input (X, from column 0 to 7) and output (Y , the last column)
X = dataSet[: , 0:8]
Y = dataSet[: , 8]

"""
The neural network should obtain the value in Y 
    starting from the input parameters
The neural network is make by different layers:
    -input layer -> the dim must be equal to the number of input params
    - middle layers
    - output layer
We will create a fully connected network structure with three layers:
    -> a fully connected layer is defined using the Dense class
We will use the 'rectified linear unit activation function' referred to 
    as ReLu on the first two layers and the Sigmoid function on the 
    output layer (with Sigmoid function we assure the output is 
    between 0 and 1 -> easy to map)
The first hidden layer has 12 nodes (ReLu activation function)
The second hidden layer has 8 nodes (ReLu activation function)
The output layer has 1 node (sigmoid activation function) 
"""

# Define the keras model (a sequential model)
model = Sequential()
model.add(Dense(12 , input_dim = 8 , activation = 'relu'))
model.add(Dense(8 , activation = 'relu'))
model.add(Dense(4 , activation = 'relu'))
model.add(Dense(1 , activation = 'sigmoid'))

# Now we can compile the model
model.compile(loss = 'binary_crossentropy' , optimizer = 'adam' , metrics = ['accuracy'])

"""
Sample: a single row of data
Batch: number of rows of data to work through before updating
        the internal model parameters
Epoch: number of times that the learning algorithm will work 
        through the entire training dataSet
"""
n_epochs = 500
batch_s = 10
# Now we will execute the model on some data (fit function)
model.fit(X , Y , epochs = n_epochs , batch_size = batch_s)
# Now the neural network is trained

# We can valuate the performance of the network on the same dataSet
loss , accuracy = model.evaluate(X , Y)
print('Accuracy: %.2f' % (accuracy * 100))

















