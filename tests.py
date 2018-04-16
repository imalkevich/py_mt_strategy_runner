#!/usr/bin/env python

""" Tests for py_my_strategy_runner. """

import inspect
import os
import unittest

from datetime import datetime

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


if __name__ == '__main__':
    unittest.main()