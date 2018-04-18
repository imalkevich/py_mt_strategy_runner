#!/usr/bin/env python

"""
Multilayer perceptron using the window method,
can predict a couple of next trades based on existing history.
"""

import math
import numpy

from keras.models import Sequential
from keras.layers import Dense

class MultilayerPerceptron(object):
    def __init__(self, dataset):
        self.dataset = dataset
        self.model = None

    def _create_dataset(self, dataset, look_back):
        dataX, dataY = [], []
        for i in range(len(dataset)-look_back-1):
            a = dataset[i:(i+look_back), 0]
            dataX.append(a)
            dataY.append(dataset[i + look_back, 0])
        return numpy.array(dataX), numpy.array(dataY)

    def train(self, look_back = 30, train_history = 500):
        # split into train and test sets
        train_size = int(len(self.dataset) * 0.9)
        train, test = self.dataset[0:train_size,:], self.dataset[train_size:len(self.dataset),:]

        # reshape dataset
        trainX_full, trainY_full = self._create_dataset(train, look_back)
        testX_full, testY_full = self._create_dataset(test, look_back)

        trainX = trainX_full[-train_history:]
        trainY = trainY_full[-train_history:]

        testX = testX_full
        testY = testY_full

        # create and fit Multilayer Perceptron model
        model = Sequential()
        model.add(Dense(24, input_dim=look_back, activation='relu'))
        model.add(Dense(12, activation='relu'))
        model.add(Dense(1))
        model.compile(loss='mean_squared_error', optimizer='adam')
        model.fit(trainX, trainY, epochs=200, batch_size=64, verbose=0, validation_data=(testX, testY), shuffle=False)

        # Estimate model performance
        trainScore = model.evaluate(trainX, trainY, verbose=0)
        testScore = model.evaluate(testX, testY, verbose=0)

        return { 
            'TrainScore': { 'MSE': trainScore, 'RMSE': math.sqrt(trainScore) },
            'TestScore': { 'MSE': testScore, 'RMSE': math.sqrt(testScore) },
        }

