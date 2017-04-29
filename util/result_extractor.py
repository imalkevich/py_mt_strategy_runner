""" extract results and store them in csv file """

import re
import glob
from os import path
from .report import report_file_name_template, report_file_folder
from .params import RUNNER_FOLDER

reNumber = r'([-+]?\d+[.]?\d*)'
reNumberWithPercent = r'([-+]?\d+[.]?\d*) (\([-+]?\d+[.]?\d*%\))'
reBoolean = r'(true|false)'

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
    for terminal_path, result_id in terminals.items():
        report_folder = path.join(terminal_path, report_file_name_template
                                  .format(RUNNER_FOLDER, report_file_folder, result_id))
        for report_file in glob.glob(report_folder):
            lines = ''.join(open(report_file, 'r').readlines())
            data = dict()
            data['ResultId'] = result_id
            for k, val in dict_params.items():
                search = re.search(val, lines)
                if search:
                    data[k] = search.group(1)
                else:
                    data[k] = "NA"
            results.append(data)

    return results

