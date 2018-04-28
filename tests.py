#!/usr/bin/env python

""" Tests for py_my_strategy_runner. """

import inspect
import os
import pandas as pd
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
from db.run_result import get_run_result_trades_summary_by_configuration_id

from main import process, reset_runner, smart_refresh_trades

from machine_learning.analytics import TradeResultPredictor, MultilayerPerceptron

from util import terminal
from util.result_extractor import prepare_results


from terminal.runner import Metatrader4, SmartMetatrader4
from terminal.reporting import TradesDiffReporter

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
        expected_df = pd.DataFrame([
            {'col1': 'row1_col1_result', 'col2': 'row1_col2_result'}, 
            {'col1': 'row2_col1_result', 'col2': 'row2_col2_result'}
        ])
        assert_frame_equal(df, expected_df)
        mock_cursor.execute.assert_called_with(mock.ANY, 'fake_result_id')
        mock_cursor.fetchall.assert_called_once()
        mock_cursor.close.assert_called_once()

    @mock.patch('db.run_result._get_connection')
    def test_get_run_result_trades_summary_by_configuration_id(self, mock_get_connection):
        # arrange
        mock_cursor = mock.MagicMock()
        mock_cursor.description = ((['ResultId']), (['NumTrades']), (['MaxCloseTime']))
        mock_cursor.fetchall = mock.MagicMock(return_value=((['1', '100', 'Today']), (['2', '200', 'Yesterday'])))
        mock_connection = mock.MagicMock()
        mock_connection.cursor = mock.MagicMock(return_value=mock_cursor)
        mock_get_connection.return_value = mock_connection

        # act
        df = get_run_result_trades_summary_by_configuration_id('fake_configuration_id')

        # assert
        expected_df = pd.DataFrame([
            {'ResultId': '1', 'NumTrades': '100', 'MaxCloseTime': 'Today' }, 
            {'ResultId': '2', 'NumTrades': '200', 'MaxCloseTime': 'Yesterday'}
        ])
        assert_frame_equal(df, expected_df)
        mock_cursor.execute.assert_called_with(mock.ANY, 'fake_configuration_id')
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

class MainTestClass(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    @mock.patch('main.run_result')
    @mock.patch('main.glob')
    @mock.patch('main.os')
    def test_reset_runner(self, mock_os, mock_glob, mock_run_result):
        # arrange
        mock_run_result.remove_run_result_trades_by_configuration_id = mock.MagicMock()
        mock_run_result.reset_run_results_by_configuration_id = mock.MagicMock()
        mock_glob.glob = mock.MagicMock(return_value=['file_1', 'file_2'])
        mock_os.remove = mock.MagicMock()

        # act
        reset_runner('some_configuration_id')

        # assert
        mock_run_result.remove_run_result_trades_by_configuration_id.assert_called_with('some_configuration_id')
        mock_run_result.reset_run_results_by_configuration_id.assert_called_with('some_configuration_id')
        mock_glob.glob.assert_called_with('/saved_models/*')
        mock_os.remove.assert_has_calls([mock.call('file_1'), mock.call('file_2')])

    @mock.patch('main.run')
    @mock.patch('main.run_result')
    @mock.patch('main.terminal')
    def test_smart_refresh_trades(self, mock_terminal, mock_run_result, mock_run):
        # arrange
        runs = [{'RunId': 1, 'TestDateFrom': '2018.04.01'}]
        mock_run.get_by_configuration_id = mock.MagicMock(return_value=runs)

        trades = pd.DataFrame({
            'RunId': [1, 1],
            'ResultId': [1, 2],
            'NumTrades': [10, 15],
            'MaxCloseTime': [datetime(2018, 4, 27, 9, 15, 0), datetime(2018, 4, 28, 9, 20, 0)]
        })
        mock_run_result.get_run_result_trades_summary_by_configuration_id = mock.MagicMock(return_value=trades)
        mock_run_result.delete_trades_by_rusult_id_and_close_time = mock.MagicMock()
        mock_run_result.reset_run_results_by_configuration_id = mock.MagicMock()

        def side_effect(*args):
            if args[1] == 1:
                return datetime(2018, 4, 26, 0, 0, 0)
            elif args[1] == 2:
                return datetime(2018, 4, 27, 0, 0, 0)
            raise ValueError('Incorrect argument passed')
        mock_terminal.get_run_result_date_from = mock.MagicMock(side_effect=side_effect)

        # act
        smart_refresh_trades('id')

        # assert
        mock_run.get_by_configuration_id.assert_called_with('id')
        mock_run_result.get_run_result_trades_summary_by_configuration_id.assert_called_with('id')
        self.assertEqual(2, mock_terminal.get_run_result_date_from.call_count)
        mock_run_result.delete_trades_by_rusult_id_and_close_time.assert_has_calls([
            mock.call(1, datetime(2018, 4, 26, 0, 0, 0)), 
            mock.call(2, datetime(2018, 4, 27, 0, 0, 0))
        ])
        mock_run_result.reset_run_results_by_configuration_id.assert_called_with('id')

    def test_process(self):

        # act
        process(4, False, 5)

class Metatrader4TestClass(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    @mock.patch('terminal.runner.launch')
    def test_create_ini_file(self, mock_launch):
        # arrange
        mock_launch.create_ini_file = mock.MagicMock(return_value=True)
        mt4 = Metatrader4('id', ['teminal_1'], verbose=False)

        # act
        ini_file = mt4._create_ini_file('data_path', 'run_result_id', 'date_from', 'date_to', 'symbol', 'set_file_name')

        # assert
        self.assertEqual(True, ini_file)
        mock_launch.create_ini_file.assert_called_with('data_path', 'run_result_id', 'date_from', 'date_to', 'symbol', 'set_file_name')

    def test_get_run_result_date_from(self):
        # arrange
        mt4 = Metatrader4('id', ['teminal_1'], verbose=False)

        # act
        run_date_from = mt4._get_run_result_date_from('run_date_from', 'run_result_id')

        # assert
        self.assertEqual('run_date_from', run_date_from)

class TradesDiffReporterTestClass(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_get_new_column_names(self):
        # arrange
        cols = ['ResultId', 'NumTrades', 'MaxCloseTime']

        # act
        new_cols = TradesDiffReporter('id')._get_new_column_names('before', cols)

        # assert
        expected_cols = { 'ResultId': 'ResultId', 'NumTrades': 'before_NumTrades', 'MaxCloseTime': 'before_MaxCloseTime' }
        self.assertDictEqual(expected_cols, new_cols)

    def test_generate_report_no_diff(self):
        # arrange
        reporter = TradesDiffReporter('id')
        before = pd.DataFrame({
            'ResultId': [1, 2, 3],
            'before_NumTrades': [10, 15, 20],
            'before_MaxCloseTime': [datetime(2018, 4, 27, 9, 15, 0), datetime(2018, 4, 27, 9, 20, 0), datetime(2018, 4, 27, 9, 25, 0)]
        })

        after = pd.DataFrame({
            'ResultId': [1, 2, 3],
            'after_NumTrades': [10, 15, 20],
            'after_MaxCloseTime': [datetime(2018, 4, 27, 9, 15, 0), datetime(2018, 4, 27, 9, 20, 0), datetime(2018, 4, 27, 9, 25, 0)]
        })

        # act
        report = reporter._generate_report(before, after)

        # assert
        self.assertFalse(report['hasNewTrades'])

    def test_generate_report_diff_number_trades(self):
        # arrange
        reporter = TradesDiffReporter('id')
        before = pd.DataFrame({
            'ResultId': [1, 2, 3],
            'before_NumTrades': [10, 15, 20],
            'before_MaxCloseTime': [datetime(2018, 4, 27, 9, 15, 0), datetime(2018, 4, 27, 9, 20, 0), datetime(2018, 4, 27, 9, 25, 0)]
        })

        after = pd.DataFrame({
            'ResultId': [1, 2, 3],
            'after_NumTrades': [10, 15, 21],
            'after_MaxCloseTime': [datetime(2018, 4, 27, 9, 15, 0), datetime(2018, 4, 27, 9, 20, 0), datetime(2018, 4, 27, 9, 27, 0)]
        })

        # act
        report = reporter._generate_report(before, after)

        # assert
        self.assertTrue(report['hasNewTrades'])

    def test_generate_report_diff_by_dates(self):
        # arrange
        reporter = TradesDiffReporter('id')
        before = pd.DataFrame({
            'ResultId': [1, 2, 3],
            'before_NumTrades': [10, 15, 20],
            'before_MaxCloseTime': [datetime(2018, 4, 27, 9, 15, 0), datetime(2018, 4, 27, 9, 20, 0), datetime(2018, 4, 27, 9, 25, 0)]
        })

        after = pd.DataFrame({
            'ResultId': [1, 2, 3],
            'after_NumTrades': [10, 15, 20],
            'after_MaxCloseTime': [datetime(2018, 4, 27, 9, 15, 0), datetime(2018, 4, 27, 9, 20, 0), datetime(2018, 4, 27, 9, 27, 0)]
        })

        # act
        report = reporter._generate_report(before, after)

        # assert
        self.assertTrue(report['hasNewTrades'])

class SmartMetatrader4TestClass(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    @mock.patch('terminal.runner.terminal')
    def test_get_run_result_date_from(self, mock_terminal):
        # arrange
        mock_terminal.get_run_result_date_from_formatted = mock.MagicMock(return_value='2018.04.26')
        mt4 = SmartMetatrader4('id', ['teminal_1'], verbose=False)

        # act
        date_from = mt4._get_run_result_date_from('2018.01.01', 1)

        # assert
        self.assertEqual('2018.04.26', date_from)
        mock_terminal.get_run_result_date_from_formatted.assert_called_once()

    @mock.patch('terminal.runner.terminal')
    def test_adjust_reports(self, mock_terminal):
        # arrange
        def side_effect(*args):
            if args[1] == 1:
                return datetime(2018, 4, 26, 0, 0, 0)
            elif args[1] == 2:
                return datetime(2018, 4, 27, 0, 0, 0)
            raise ValueError('Incorrect argument passed')

        mock_terminal.get_run_result_date_from = mock.MagicMock(side_effect=side_effect)

        reports = [{
            'ResultId': 1,
            'Trades': [
                {'Time': datetime(2018, 4, 25, 9, 0, 0), 'Profit': -11.0},
                {'Time': datetime(2018, 4, 25, 17, 0, 0), 'Profit': 15.0},
                {'Time': datetime(2018, 4, 26, 3, 0, 0), 'Profit': 25.0}
            ]}, {
            'ResultId': 2,
            'Trades': [
                {'Time': datetime(2018, 4, 26, 9, 0, 0), 'Profit': -11.0},
                {'Time': datetime(2018, 4, 26, 17, 0, 0), 'Profit': 15.0},
                {'Time': datetime(2018, 4, 26, 22, 0, 0), 'Profit': 25.0}
            ]
        }]

        mt4 = SmartMetatrader4('id', ['terminal'])

        # act
        result_reports = mt4._adjust_reports('2018.04.01', reports)

        # assert
        expected_reports = [{
            'ResultId': 1,
            'Trades': [
                {'Time': datetime(2018, 4, 26, 3, 0, 0), 'Profit': 25.0}
            ]}, {
            'ResultId': 2,
            'Trades': []
        }]
        self.assertDictEqual(expected_reports[0], result_reports[0])
        self.assertDictEqual(expected_reports[1], result_reports[1])


class TerminalUtilTestClass(unittest.TestCase):
    def test_get_run_result_date_from_no_trades(self):
        # arrange
        df_run_trades = None

        # act
        date_from = terminal.get_run_result_date_from('2018.04.01', 1, df_run_trades)

        # assert
        self.assertEqual(datetime(2018, 4, 1, 0, 0, 0), date_from)

    def test_get_run_result_date_from_empty_df(self):
        # arrange
        df_run_trades = pd.DataFrame({
            'ResultId': [],
            'NumTrades': [],
            'MaxCloseTime': []
        })

        # act
        date_from = terminal.get_run_result_date_from('2018.04.01', 1, df_run_trades)

        # assert
        self.assertEqual(datetime(2018, 4, 1, 0, 0, 0), date_from)

    def test_get_run_result_date_from(self):
        # arrange
        df_run_trades = pd.DataFrame({
            'ResultId': [1],
            'MaxCloseTime': [datetime(2018, 4, 27, 9, 15, 0)]
        })

        # act
        date_from = terminal.get_run_result_date_from('2018.04.01', 1, df_run_trades)

        # assert
        self.assertEqual(datetime(2018, 4, 26, 0, 0, 0), date_from)

    @mock.patch('util.terminal.terminal')
    def test_get_run_result_date_from_formatted(self, mock_terminal):
        # arrange
        mock_terminal.get_run_result_date_from = mock.MagicMock(return_value=datetime(2018, 4, 27, 9, 15, 0))

        # act
        date_from = terminal.get_run_result_date_from_formatted('2018.01.01', 1, None)

        # assert
        self.assertEqual('2018.04.27', date_from)

if __name__ == '__main__':
    unittest.main()
