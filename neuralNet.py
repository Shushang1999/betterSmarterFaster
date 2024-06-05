import numpy as np
import matplotlib.pyplot as plt
import pickle
import networkx as nx
import pandas as pd
import find_path
import math

def data_preprocessing():
    utility = pd.read_pickle("utility.pkl")
    # print(utility)
    utility.replace(math.inf, 50, inplace=True)
    X = utility.drop(columns=["Utility"])
    # print(X)

    X_train = X.head(100000)
    X_test = X.tail(25000)
    # print(X_train)
    # print(X_test)
    # print(Y)
    Y = utility["Utility"].to_frame()
    Y_train = Y[:100000]
    Y_test = Y[100000:]
    # print(Y_train,len(Y_train))
    # print(Y_test,len(Y_test))

    # data = temp_data.temp_fun()
    # X_train = data.drop(columns=["type"])

    # Y_train = data["type"].to_frame()

    return(X_train,Y_train,X_test,Y_test)

def initialWeights(layers):
    params = {}
    np.random.seed(10)
    params["W1"] = np.random.randn(layers[0],layers[1])
    params["W2"] = np.random.randn(layers[1],layers[2])
    params["W3"] = np.random.randn(layers[2],layers[3])
    params["b1"] = np.random.randn(layers[1],)
    params["b2"] = np.random.randn(layers[2],)
    params["b3"] = np.random.randn(layers[3],)

    return(params)

def relu(arr):
    return np.maximum(0,arr)

def leaky_Relu(arr):
    return np.maximum(0.01 * arr,arr)

def sigmoid(Z):
    return 1/(1+np.exp(-Z))

def dSigmoid(Z):
    return(sigmoid(Z) * (1-sigmoid(Z)))

def dRelu(x):
    x[x<=0] = 0
    x[x>0] = 1
    return x

def tanH(x):
    return(np.tanh(x))

def dTanH(x):
    return (1-np.tanh(x)**2)

def dLeekyRelu(x):
    x[x<=0] = 0.01
    x[x>0] = 1
    return x

def forwardPropogation(X,params):
    inter_params = {}
    # print(params["b1"].shape)
    Z1 = np.dot(X,params["W1"]) + params["b1"]
    # print(Z1.shape)
    A1 = tanH(Z1)
    # print(A1.shape)
    Z2 = np.dot(A1,params["W2"]) + params["b2"]
    A2 = tanH(Z2)
    Z3 = np.dot(A2,params["W3"]) + params["b3"]
    yhat = Z3

    inter_params["Z1"] = Z1
    inter_params["A1"] = A1
    inter_params["Z2"] = Z2
    inter_params["A2"] = A2
    inter_params["Z3"] = Z3
    inter_params["W1"] = params["W1"]
    inter_params["W2"] = params["W2"]
    inter_params["W3"] = params["W3"]

    return(yhat,inter_params)

def backPropogation(X_train,yhat,Y,inter_params,params,learning_rate):
    dl = (2 * np.subtract(Y,yhat).to_numpy()) / len(X_train)
    dZ3 = dl
    dW3 = (inter_params["A2"].transpose().dot(dZ3))
    dB3 = np.sum(dZ3,axis=0,keepdims=True)

    dZ2 = np.array(dZ3.dot(inter_params["W3"].transpose()) * dTanH(inter_params["Z2"]))
    dW2 = (inter_params["A1"].transpose().dot(dZ2))
    dB2 = np.sum(dZ2,axis=0,keepdims=True)

    dZ1 = np.array(dZ2.dot(inter_params["W2"].transpose()) * dTanH(inter_params["Z1"]))
    dW1 = (X_train.transpose().dot(dZ1))
    dB1 = np.sum(dZ1,axis=0,keepdims=True)

    params["W1"] = params["W1"] + learning_rate * dW1
    params["W2"] = params["W2"] + learning_rate * dW2
    params["W3"] = params["W3"] + learning_rate * dW3
    params["b1"] = params["b1"] + learning_rate * dB1
    params["b2"] = params["b2"] + learning_rate * dB2
    params["b3"] = params["b3"] + learning_rate * dB3

    return(params)


def meanSquaredErrorLoss(Y,yhat):
    y_diff = np.subtract(Y,yhat).to_numpy()
    sum = 0
    for ele in y_diff:
        sum += (ele[0] * ele[0])
    return(sum/len(Y))

def NeuralNet():
    layers = [2,4,3,1]
    learning_rate = 0.001
    iterations = 5000
    loss = []
    params = initialWeights(layers)
    X_train,Y_train,X_test,Y_test = data_preprocessing()
    # print(X_train.shape)
    for i in range(iterations):
        print(i)
        yhat,inter_params = forwardPropogation(X_train,params)
        loss.append(meanSquaredErrorLoss(Y_train,yhat))
        params = backPropogation(X_train,yhat,Y_train,inter_params,params,learning_rate)
    print(loss)
    # print(Y_train)
    # print(yhat)
    plot_loss(loss)

    with open("neural_weights_1","wb") as utility_file:
        pickle.dump(params,utility_file,protocol=pickle.HIGHEST_PROTOCOL)

def test():
    with open("neural_weights","rb") as handle:
        params = pickle.load(handle)
    X_train,Y_train,X_test,Y_test = data_preprocessing()
    yhat,inter_params = forwardPropogation(X_test,params)
    print("loss" ,(meanSquaredErrorLoss(Y_test,yhat)))


def plot_loss(loss):
    plt.plot(loss)
    plt.xlabel("Iteration")
    plt.ylabel("loss")
    plt.title("Loss curve for training")
    plt.show()  
    

if __name__ == "__main__":
    # with open("neural_weights","rb") as handle:
    #     weights = pickle.load(handle)
    # x_list = [12,15]
    # x = pd.DataFrame(x_list).transpose()
    # # print(type(weights["W1"]))
    # # print(x.shape)
    # # print(weights["W1"].shape)
    # # print(weights["b1"].shape)
    # # temp = np.dot(x,weights["W1"])
    # # Z1 = np.dot(x,weights["W1"]) + weights["b1"]
    # # print(Z1)

    # y,inter_params = forwardPropogation(x,weights)
    # print(y[0][0])

    NeuralNet()
    # test()
