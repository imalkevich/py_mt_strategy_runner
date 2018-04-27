#!/usr/bin/env python

""" Tests for py_my_strategy_runner. """

import inspect
import os
import pandas
import numpy as np
import unittest
import unittest.mock as mock

from datetime import datetime
from decimal import Decimal
from numpy.testing import assert_array_equal
from pandas.util.testing import assert_frame_equal

from db.run_result import add_run_result_trade, remove_run_result_trades_by_configuration_id, reset_run_results_by_configuration_id
from db.run_result import get_completed_run_results_by_configuration_id
from db.run_result import get_run_result_trades_by_result_id

from machine_learning.analytics import TradeResultPredictor, MultilayerPerceptron

from util.result_extractor import prepare_results

class ResultExtractorTestCase(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_prepare_results(self):
        # arrange
        data_path = os.path.join(
            os.path.dirname(inspect.getfile(self.__class__)),
            'test_fixture')
        terminals = { data_path: 'test' }

        # act
        results = prepare_results(terminals)

        # assert
        self.assertEqual(len(results), 1)
        report = results[0]
        self.assertEqual(report['TotalNetProfit'], '1145.19')
        self.assertEqual(len(report['Trades']), 17)
        trades = [
            { 'Time': datetime(2018, 1, 3, 21, 15, 0), 'Profit': 380.0 },
            { 'Time': datetime(2018, 1, 11, 23, 30, 0), 'Profit': 124.80 },
            { 'Time': datetime(2018, 1, 12, 15, 46, 0), 'Profit': 21.10 },
            { 'Time': datetime(2018, 1, 12, 15, 46, 0), 'Profit': 548.60 },
            { 'Time': datetime(2018, 1, 16, 1, 30, 0), 'Profit': 53.17 },
            { 'Time': datetime(2018, 1, 16, 4, 30, 0), 'Profit': 276.52 },
            { 'Time': datetime(2018, 1, 16, 9, 8, 0), 'Profit': 22.90 },
            { 'Time': datetime(2018, 1, 18, 7, 0, 0), 'Profit': -813.29 },
            { 'Time': datetime(2018, 1, 23, 5, 23, 0), 'Profit': 21.30 },
            { 'Time': datetime(2018, 1, 23, 7, 12, 0), 'Profit': 21.30 },
            { 'Time': datetime(2018, 1, 25, 9, 31, 0), 'Profit': 21.40 },
            { 'Time': datetime(2018, 1, 25, 9, 56, 0), 'Profit': 21.40 },
            { 'Time': datetime(2018, 1, 25, 10, 26, 0), 'Profit': 21.40 },
            { 'Time': datetime(2018, 1, 25, 19, 22, 0), 'Profit': 21.50 },
            { 'Time': datetime(2018, 1, 25, 20, 28, 0), 'Profit': 21.50 },
            { 'Time': datetime(2018, 1, 30, 2, 45, 0), 'Profit': 359.29 },
            { 'Time': datetime(2018, 1, 30, 11, 38, 0), 'Profit': 22.30 },
        ]
        self.assertEqual(report['Trades'], trades)

class DatabaseTestCase(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_add_run_result_trade(self):
        # arrange
        mock_cursor = mock.MagicMock()
        trade = { 'Time': 'someTime', 'Profit': 'someProfit' }
        
        # act
        add_run_result_trade(mock_cursor, 'testResultId', trade)

        # assert
        mock_cursor.execute.assert_called_with(mock.ANY, 'testResultId', 'someTime', 'someProfit')

    @mock.patch('db.run_result._get_connection')
    def test_remove_run_result_trades_by_configuration_id(self, mock_get_connection):
        # arrange
        mock_cursor = mock.MagicMock()
        mock_connection = mock.MagicMock()
        mock_connection.cursor = mock.MagicMock(return_value=mock_cursor)
        mock_get_connection.return_value = mock_connection

        # act
        remove_run_result_trades_by_configuration_id('fake_configuration_id')

        # assert
        mock_cursor.execute.assert_called_with(mock.ANY, 'fake_configuration_id')
        mock_cursor.close.assert_called_once()
        mock_connection.commit.assert_called_once()

    @mock.patch('db.run_result._get_connection')
    def test_reset_run_results_by_configuration_id(self, mock_get_connection):
        # arrange
        mock_cursor = mock.MagicMock()
        mock_connection = mock.MagicMock()
        mock_connection.cursor = mock.MagicMock(return_value=mock_cursor)
        mock_get_connection.return_value = mock_connection

        # act
        reset_run_results_by_configuration_id('fake_configuration_id')

        # assert
        mock_cursor.execute.assert_called_with(mock.ANY, 'fake_configuration_id')
        mock_cursor.close.assert_called_once()
        mock_connection.commit.assert_called_once()

    @mock.patch('db.run_result._get_connection')
    def test_get_completed_run_results_by_configuration_id(self, mock_get_connection):
        # arrange
        mock_cursor = mock.MagicMock()
        mock_cursor.description = ((['col1']), (['col2']))
        mock_cursor.fetchall = mock.MagicMock(return_value=((['row1_col1_result', 'row1_col2_result']), (['row2_col1_result', 'row2_col2_result'])))
        mock_connection = mock.MagicMock()
        mock_connection.cursor = mock.MagicMock(return_value=mock_cursor)
        mock_get_connection.return_value = mock_connection

        # act
        rows = get_completed_run_results_by_configuration_id('fake_configuration_id')

        # assert
        self.assertEqual(rows, [{'col1': 'row1_col1_result', 'col2': 'row1_col2_result'}, {'col1': 'row2_col1_result', 'col2': 'row2_col2_result'}])
        mock_cursor.execute.assert_called_with(mock.ANY, 'fake_configuration_id')
        mock_cursor.fetchall.assert_called_once()
        mock_cursor.close.assert_called_once()

    @mock.patch('db.run_result._get_connection')
    def test_get_run_result_trades_by_result_id(self, mock_get_connection):
        # arrange
        mock_cursor = mock.MagicMock()
        mock_cursor.description = ((['col1']), (['col2']))
        mock_cursor.fetchall = mock.MagicMock(return_value=((['row1_col1_result', 'row1_col2_result']), (['row2_col1_result', 'row2_col2_result'])))
        mock_connection = mock.MagicMock()
        mock_connection.cursor = mock.MagicMock(return_value=mock_cursor)
        mock_get_connection.return_value = mock_connection

        # act
        df = get_run_result_trades_by_result_id('fake_result_id')

        # assert
        expected_df = pandas.DataFrame([
            {'col1': 'row1_col1_result', 'col2': 'row1_col2_result'}, 
            {'col1': 'row2_col1_result', 'col2': 'row2_col2_result'}
        ])
        assert_frame_equal(df, expected_df)
        mock_cursor.execute.assert_called_with(mock.ANY, 'fake_result_id')
        mock_cursor.fetchall.assert_called_once()
        mock_cursor.close.assert_called_once()

class TradeResultPredictorTestCase(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_run(self):
        # arrange
        predictor = TradeResultPredictor(4, verbose=2)

        # act
        #predictor.run()

    @mock.patch('machine_learning.analytics.smtplib')
    def test_send_notification(self, mock_smtplib):
        # arrange
        predictor = TradeResultPredictor('some_configuration_id')

        mock_server = mock.MagicMock()
        dummySMTP = mock.MagicMock(return_value=mock_server)

        mock_smtplib.SMTP = dummySMTP

        # act
        predictor._send_notification('Test email', 'Test email body', 'smtp_user', 'smtp_password', ['ihar.malkevich@thomsonreuters.com'])

        # assert
        mock_smtplib.SMTP.assert_called_with('smtp.gmail.com', 587)
        mock_server.ehlo.assert_called_once()
        mock_server.starttls.assert_called_once()
        mock_server.login.assert_called_with('smtp_user', 'smtp_password')
        mock_server.send_message.assert_called_once()
        mock_server.quit.assert_called_once()

class MultilayerPerceptronTestCase(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_create_dataset(self):
        # arrange
        perceptron = MultilayerPerceptron('result_id', None)

        source = np.array([
            [Decimal('1.00')], [Decimal('2.00')], [Decimal('3.00')], [Decimal('4.00')], [Decimal('5.00')],
            [Decimal('6.00')], [Decimal('7.00')], [Decimal('8.00')]
        ])

        # act
        (dataX, dataY) = perceptron._create_dataset(source, look_back=3)

        # assert
        expectedX = np.array([
            [Decimal('1.00'), Decimal('2.00'), Decimal('3.00')],
            [Decimal('2.00'), Decimal('3.00'), Decimal('4.00')],
            [Decimal('3.00'), Decimal('4.00'), Decimal('5.00')],
            [Decimal('4.00'), Decimal('5.00'), Decimal('6.00')]
        ])
        expectedY = np.array([
            Decimal('4.00'),
            Decimal('5.00'),
            Decimal('6.00'),
            Decimal('7.00')
        ])
        assert_array_equal(dataX, expectedX)
        assert_array_equal(dataY, expectedY)

    def test_predict(self):
        # arrange
        def side_effect(*args):
            if np.array_equal(args[0], np.array([[Decimal('1.00'), Decimal('2.00'), Decimal('3.00'), Decimal('4.00'), Decimal('5.00')]])):
                return np.array([[Decimal('6.00')]])
            elif np.array_equal(args[0], np.array([[Decimal('2.00'), Decimal('3.00'), Decimal('4.00'), Decimal('5.00'), Decimal('6.00')]])):
                return np.array([[Decimal('7.00')]])
            elif np.array_equal(args[0], np.array([[Decimal('3.00'), Decimal('4.00'), Decimal('5.00'), Decimal('6.00'), Decimal('7.00')]])):
                return np.array([[Decimal('8.00')]])
            return 0

        dataset = np.array([
            [Decimal('1.00')], [Decimal('2.00')], [Decimal('3.00')], [Decimal('4.00')], [Decimal('5.00')]
        ])
        perceptron = MultilayerPerceptron('result_id', dataset, look_back=5)
        perceptron.model = mock.MagicMock()
        perceptron.model.predict = mock.MagicMock(side_effect=side_effect)

        # act
        predicted = perceptron.predict(look_forth=3)

        # assert
        self.assertEqual(predicted, [Decimal('6.00'), Decimal('7.00'), Decimal('8.00')])

    @mock.patch('machine_learning.multilayer_perceptron.open')
    @mock.patch('machine_learning.multilayer_perceptron.path')
    @mock.patch('machine_learning.multilayer_perceptron.models')
    def test_get_trained_model_should_train_new_model_no_model_files(self, mock_models, mock_path, mock_open):
        # arrange
        mock_instance = mock.MagicMock()
        mock_models.Sequential = mock.MagicMock(return_value=mock_instance)
        mock_path.isfile.return_value = False
        mock_open.return_value = mock.MagicMock()

        perceptron = MultilayerPerceptron('result_id', None)
        sample = np.array([[1], [2]])

        # act
        model = perceptron._get_trained_model(sample, sample, sample, sample)

        # assert
        self.assertIsNotNone(model)
        mock_instance.compile.assert_called_once()
        mock_instance.fit.assert_called_once()
        mock_instance.to_json.assert_called_once()
        mock_instance.save_weights.assert_called_once()
        mock_open.assert_called_once()

    @mock.patch('machine_learning.multilayer_perceptron.open')
    @mock.patch('machine_learning.multilayer_perceptron.path')
    @mock.patch('machine_learning.multilayer_perceptron.models')
    def test_get_trained_model_should_load_existing_model_files_exist(self, mock_models, mock_path, mock_open):
        # arrange
        mock_instance = mock.MagicMock()
        mock_models.model_from_json = mock.MagicMock(return_value=mock_instance)
        mock_path.isfile.return_value = True
        mock_open.return_value = mock.MagicMock()

        perceptron = MultilayerPerceptron('result_id', None)

        # act
        model = perceptron._get_trained_model(None, None, None, None)

        # assert
        self.assertIsNotNone(model)
        mock_models.model_from_json.assert_called_once()
        mock_instance.load_weights.assert_called_once()


if __name__ == '__main__':
    unittest.main()