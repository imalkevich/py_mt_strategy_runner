""" extract results and store them in csv file """

import os
import re

from datetime import datetime

from .report import report_file_name_template, report_file_folder
from .params import RUNNER_FOLDER
from pyquery import PyQuery as pq

reNumber = r'([-+]?\d+[.]?\d*)'
reNumberWithPercent = r'([-+]?\d+[.]?\d*) (\([-+]?\d+[.]?\d*%\))'
reBoolean = r'(true|false)'
reTradeType = r'(sell|buy)'

TRADE_DATETIME_FORMAT = '%Y.%m.%d %H:%M'

dict_params = {
    'TakeProfit': r'TakeProfit='+reNumber,
    'StopLoss':  r'StopLoss='+reNumber,
    'UseStopLevels': r'UseStopLevels='+reBoolean,
    'IsMarketExecution': r'IsMarketExecution='+reBoolean,
    'SecureProfit': r'SecureProfit='+reNumber,
    'SecureProfitTriger': r'SecureProfitTriger='+reNumber,
    'MaxLossPoints': r'MaxLossPoints='+reNumber,
    'RecoveryMode': r'RecoveryMode='+reBoolean,
    'FixedLot': r'FixedLot='+reNumber,
    'AutoMM': r'AutoMM='+reNumber,
    'AutoMM_Max': r'AutoMM_Max='+reNumber,
    'MaxAnalizCount': r'MaxAnalizCount='+reNumber,
    'Risk': r'Risk='+reNumber,
    'MultiLotPercent': r'MultiLotPercent='+reNumber,
    'iMA_Period': r'iMA_Period='+reNumber,
    'iCCI_Period': r'iCCI_Period='+reNumber,
    'iATR_Period': r'iATR_Period='+reNumber,
    'iWPR_Period': r'iWPR_Period='+reNumber,
    'FilterATR': r'FilterATR='+reNumber,
    'iCCI_OpenFilter': r'iCCI_OpenFilter='+reNumber,
    'iMA_Filter_Open_a': r'iMA_Filter_Open_a='+reNumber,
    'iMA_Filter_Open_b': r'iMA_Filter_Open_b='+reNumber,
    'iWPR_Filter_Open_a': r'iWPR_Filter_Open_a='+reNumber,
    'iWPR_Filter_Open_b': r'iWPR_Filter_Open_b='+reNumber,
    'Price_Filter_Close': r'Price_Filter_Close='+reNumber,
    'iWPR_Filter_Close': r'iWPR_Filter_Close='+reNumber,
    'TotalNetProfit': r'<td>Total net profit</td><td align=right>'+reNumber+'</td>',
    'GrossProfit': r'<td>Gross profit</td><td align=right>'+reNumber+'</td>',
    'GrossLoss': r'<td>Gross loss</td><td align=right>'+reNumber+'</td>',
    'ProfitFactor': r'<td>Profit factor</td><td align=right>'+reNumber+'</td>',
    'ExpectedPayoff': r'<td>Expected payoff</td><td align=right>'+reNumber+'</td>',
    'AbsoluteDrawdown': r'<td>Absolute drawdown</td><td align=right>'+reNumber+'</td>',
    'MaximalDrawdown': r'<td>Maximal drawdown</td><td align=right>'+reNumberWithPercent+'</td>',
    'TotalTrades': r'<td>Total trades</td><td align=right>'+reNumber+'</td>'
}

def prepare_results(terminals):
    """ prepare report from result files """
    results = []
    for data_path, result_id in terminals.items():
        report_file_name = os.path.join(data_path, report_file_name_template
                                  .format(RUNNER_FOLDER, report_file_folder, result_id))

        if os.path.isfile(report_file_name):
            lines = ''
            with open(report_file_name, 'r') as f:
                lines = ''.join(f.readlines())
            data = dict()
            data['ResultId'] = result_id
            for k, val in dict_params.items():
                search = re.search(val, lines)
                if search:
                    data[k] = search.group(1)
                else:
                    data[k] = None

            trades = []
            html = pq(lines)
            rows = html('table:eq(1) tr')
            new_trade = None
            type_counter = 0
            close_counter = 0
            for row in rows:
                row = pq(row)
                trade_type = row('td:eq(2)').text().strip()
                profit_text = row('td:eq(8)').text().strip()
                if len(trade_type) and re.search(reTradeType, trade_type) != None:
                    type_counter += 1
                    open_time = datetime.strptime(row('td:eq(1)').text().strip(), TRADE_DATETIME_FORMAT)
                    new_trade = { 'OpenTime': open_time, 'Type': trade_type }
                if len(profit_text) and re.search(reNumber, profit_text) != None:
                    close_counter += 1
                    if type_counter != close_counter:
                        raise AssertionError('report_extractor - invalid handling of HTML')
                    close_time = datetime.strptime(row('td:eq(1)').text().strip(), TRADE_DATETIME_FORMAT)
                    profit = float(profit_text)
                    new_trade['CloseTime'] = close_time
                    new_trade['Profit'] = profit
                    trades.append(new_trade)
                    
                    # reset new_trade
                    new_trade = None

            data['Trades'] = trades

            results.append(data)

    return results

