import sys
import os
import datetime
import csv
from db.run import get_by_configuration_id
from db.connection import get_connection

CONFIGURATION_ID = 2 #int(sys.argv[1])
TARGET_FORLDER = "d:\\MyProjects\\py_mt_strategy_runner\\output\\" #sys.argv[2]

RUNS = get_by_configuration_id(CONFIGURATION_ID)

_cnxn = get_connection()
cursor = _cnxn.cursor()

tsql = """
select
	rr.TotalNetProfit as TotalNetProfit,
	rr.AbsoluteDrawdown,
	rr.MaximalDrawdown,
	rr.TotalTrades as TotalTrades,

	op.TakeProfit as TakeProfit,
	op.StopLoss as StopLoss,
	op.UseStopLevels as UseStopLevels,
	op.SecureProfit as SecureProfit,
	op.SecureProfitTriger as SecureProfitTriger,
	op.MaxLossPoints as MaxLossPoints,
	op.RecoveryMode as RecoveryMode,
	op.FixedLot as FixedLot,
	op.AutoMM as AutoMM,
	op.AutoMM_Max as AutoMM_Max,
	op.Risk as Risk,
	op.MultiLotPercent as MultiLotPercent,
	op.iMA_Period as iMA_Period,
	op.iCCI_Period as iCCI_Period,
	op.iATR_Period as iATR_Period,
	op.iWPR_Period as iWPR_Period,
	op.FilterATR as FilterATR,
	op.iCCI_OpenFilter as iCCI_OpenFilter,
	op.iMA_Filter_Open_a as iMA_Filter_Open_a,
	op.iMA_Filter_Open_b as iMA_Filter_Open_b,
	op.iWPR_Filter_Open_a as iWPR_Filter_Open_a,
	op.iWPR_Filter_Open_b as iWPR_Filter_Open_b,
	op.Price_Filter_Close as Price_Filter_Close,
	op.iWPR_Filter_Close as iWPR_Filter_Close
from
	wsrt_run_result rr
	inner join wsrt_configuration_option op on rr.OptionId = op.OptionId
where
	rr.RunFinishDateTimeUtc IS NOT NULL
	and rr.RunId = ?
order by 
	op.iMA_Period
"""

for run in RUNS:
    run_id = run['RunId']
    date_from = run['TestDateFrom']

    period = datetime.datetime.strptime(date_from, '%Y.%m.%d')

    os.makedirs(os.path.join(TARGET_FORLDER, period.strftime('%Y')), exist_ok=True)

    file_name = os.path.join(TARGET_FORLDER, period.strftime('%Y'),
                             period.strftime('%b_%Y')+'.csv')

    with open(file_name, 'w', newline='') as fout:
        writer = csv.writer(fout)
        with cursor.execute(tsql, run_id):
            #rows = cursor.fetchall()
            writer.writerow([column[0] for column in cursor.description]) # heading row
            writer.writerows(cursor.fetchall())

input("press Enter to exit ...")






