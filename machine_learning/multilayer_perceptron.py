#!/usr/bin/env python

"""
Multilayer perceptron using the window method,
can predict a couple of next trades based on existing history.
"""

import decimal
import inspect
import math
import numpy

from os import path
from os.path import dirname

from keras import models
from keras.layers import Dense

class MultilayerPerceptron(object):
    def __init__(self, result_id, dataset, look_back = 30, train_history = 500, verbose = 0):
        self.result_id = result_id
        self.dataset = dataset
        self.look_back = look_back
        self.train_history = train_history
        self.verbose = verbose
        self.model = None

    def _create_dataset(self, dataset, look_back):
        dataX, dataY = [], []
        for i in range(len(dataset)-look_back-1):
            a = dataset[i:(i+look_back), 0]
            dataX.append(a)
            dataY.append(dataset[i + look_back, 0])
        return numpy.array(dataX), numpy.array(dataY)

    def _get_trained_model(self, trainX, trainY, testX, testY):
        parent_path = dirname(dirname(inspect.getfile(self.__class__)))
        model_file_name = path.join(parent_path,
            'saved_models',
            '{}_model.json'.format(self.result_id))
        weights_file_name = path.join(parent_path,
            'saved_models',
            '{}_model_weights.h5'.format(self.result_id))
        
        model = None

        if not path.isfile(model_file_name) \
            or not path.isfile(weights_file_name):
            # fix random seed for reproducibility
            numpy.random.seed(8)
            
            # create and fit Multilayer Perceptron model
            model = models.Sequential()
            model.add(Dense(24, input_dim=self.look_back, activation='relu'))
            model.add(Dense(12, activation='relu'))
            model.add(Dense(1))
            model.compile(loss='mean_squared_error', optimizer='adam')

            # we have enough data for validation based on look_back
            if testX.shape[0]:
                model.fit(trainX, trainY, epochs=200, batch_size=64, verbose=self.verbose, validation_data=(testX, testY), shuffle=False)
            else:
                model.fit(trainX, trainY, epochs=200, batch_size=64, verbose=self.verbose, shuffle=False)

            # serialize model to JSON
            with open(model_file_name, 'w') as json_file:
                json_file.write(model.to_json())
            
            # serialize weights to HDF5
            model.save_weights(weights_file_name)
        else:
            with open(model_file_name, 'r') as json_file:
                model = models.model_from_json(json_file.read())
            model.load_weights(weights_file_name)
            model.compile(loss='mean_squared_error', optimizer='adam')

        return model

    def train(self):
        # split into train and test sets
        train_size = int(len(self.dataset) * 0.9)
        train, test = self.dataset[0:train_size,:], self.dataset[train_size:len(self.dataset),:]

        # reshape dataset
        trainX_full, trainY_full = self._create_dataset(train, self.look_back)
        testX_full, testY_full = self._create_dataset(test, self.look_back)

        trainX = trainX_full[-self.train_history:]
        trainY = trainY_full[-self.train_history:]

        testX = testX_full
        testY = testY_full

        model = self._get_trained_model(trainX, trainY, testX, testY)

        # Estimate model performance
        trainScore = model.evaluate(trainX, trainY, verbose=0)
        testScore = None
        if testX.shape[0]:
            testScore = model.evaluate(testX, testY, verbose=0)

        self.model = model

        result = { 'TrainScore': { 'MSE': trainScore, 'RMSE': math.sqrt(trainScore) } }
        if testScore is not None:
            result['TestScore'] = { 'MSE': testScore, 'RMSE': math.sqrt(testScore) }
        else:
            result['TestScore'] = { 'MSE': 'N/A', 'RMSE': 'N/A' }

        return result

    def predict(self, look_forth=3):
        history_trades = self.dataset[-self.look_back:, 0]
        predicted_trades = []
        for _ in range(look_forth):
            predicted = round(numpy.float(self.model.predict(numpy.array(history_trades).reshape(1, -1))[0][0]), 2)
            predicted = decimal.Decimal('%.4g' % predicted)
            predicted_trades.append(predicted)
            history_trades = numpy.append(history_trades[1:], [predicted])

        return predicted_trades

