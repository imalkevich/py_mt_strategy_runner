""" """

from string import Template

param_grid = {
    "TakeProfit": [26], # 26
    "StopLoss": [120], # 120
    "UseStopLevels": [1],
    "SecureProfit": [1], # 1
    "SecureProfitTriger": [10], # 10
    "MaxLossPoints": [-65],
    "RecoveryMode": [0],
    "FixedLot": [1.0],
    "AutoMM": [20.0],
    "AutoMM_Max": [20.0],
    "Risk": [25.0],
    "MultiLotPercent": [1.1],

    #_Periods=Периоды индикаторов
    "iMA_Period": range(50, 251, 1), # 75
    "iCCI_Period": [18], # 18
    "iATR_Period": [14], # 14
    "iWPR_Period": [11], # 11

    #Расширенные параметры оптимизации
    #_AddOpenFilters=---
    "FilterATR": [6], # 6
    "iCCI_OpenFilter": [150.0], # 150.0

    # _OpenOrderFilters=---
    "iMA_Filter_Open_a": [15], # 15
    "iMA_Filter_Open_b": [39], # 39
    "iWPR_Filter_Open_a": [-99], # -99
    "iWPR_Filter_Open_b": [-95], # -95

    #_CloseOrderFilters=---
    "Price_Filter_Close": [14], # 14
    "iWPR_Filter_Close": [-19] # -19
}

feature_names = list(param_grid.keys())

set_Template = Template('''Name=WallStreet Forex Robot ver. 3.8.5 FINAL (Pirate Edition)
Copy=Copyright © HELLTEAM^Pirat
Op2=Оптимизация для пары
Symbol_Op=EURUSD m15
Op=Дата оптимизации
Date=1305158400
_TP=Основные входные параметры
TakeProfit=${TakeProfit}
TakeProfit,F=0
TakeProfit,1=${TakeProfit}
TakeProfit,2=0
TakeProfit,3=0
StopLoss=${StopLoss}
StopLoss,F=0
StopLoss,1=${StopLoss}
StopLoss,2=0
StopLoss,3=0
UseStopLevels=${UseStopLevels}
UseStopLevels,F=0
UseStopLevels,1=${UseStopLevels}
UseStopLevels,2=1
UseStopLevels,3=1
IsMarketExecution=0
IsMarketExecution,F=0
IsMarketExecution,1=0
IsMarketExecution,2=1
IsMarketExecution,3=1
SecureProfit=${SecureProfit}
SecureProfit,F=0
SecureProfit,1=${SecureProfit}
SecureProfit,2=0
SecureProfit,3=0
SecureProfitTriger=${SecureProfitTriger}
SecureProfitTriger,F=0
SecureProfitTriger,1=${SecureProfitTriger}
SecureProfitTriger,2=0
SecureProfitTriger,3=0
MaxLossPoints=${MaxLossPoints}
MaxLossPoints,F=0
MaxLossPoints,1=${MaxLossPoints}
MaxLossPoints,2=0
MaxLossPoints,3=0
_MM=Настройка MM
RecoveryMode=${RecoveryMode}
RecoveryMode,F=0
RecoveryMode,1=${RecoveryMode}
RecoveryMode,2=1
RecoveryMode,3=1
FixedLot=${FixedLot}
FixedLot,F=0
FixedLot,1=${FixedLot}
FixedLot,2=0.00000000
FixedLot,3=0.00000000
AutoMM=${AutoMM}
AutoMM,F=0
AutoMM,1=0.00000000
AutoMM,2=0.00000000
AutoMM,3=0.00000000
AutoMM_Max=${AutoMM_Max}
AutoMM_Max,F=0
AutoMM_Max,1=${AutoMM_Max}
AutoMM_Max,2=0.00000000
AutoMM_Max,3=0.00000000
MaxAnalizCount=50
MaxAnalizCount,F=0
MaxAnalizCount,1=50
MaxAnalizCount,2=0
MaxAnalizCount,3=0
Risk=${Risk}
Risk,F=0
Risk,1=25.00000000
Risk,2=0.00000000
Risk,3=0.00000000
MultiLotPercent=${MultiLotPercent}
MultiLotPercent,F=0
MultiLotPercent,1=${MultiLotPercent}
MultiLotPercent,2=0.00000000
MultiLotPercent,3=0.00000000
_Periods=Периоды индикаторов
iMA_Period=${iMA_Period}
iMA_Period,F=0
iMA_Period,1=${iMA_Period}
iMA_Period,2=0
iMA_Period,3=0
iCCI_Period=${iCCI_Period}
iCCI_Period,F=0
iCCI_Period,1=${iCCI_Period}
iCCI_Period,2=0
iCCI_Period,3=0
iATR_Period=${iATR_Period}
iATR_Period,F=0
iATR_Period,1=${iATR_Period}
iATR_Period,2=0
iATR_Period,3=0
iWPR_Period=${iWPR_Period}
iWPR_Period,F=0
iWPR_Period,1=${iWPR_Period}
iWPR_Period,2=0
iWPR_Period,3=0
_Add_Op=Расширенные параметры оптимизации
_AddOpenFilters=---
FilterATR=${FilterATR}
FilterATR,F=0
FilterATR,1=${FilterATR}
FilterATR,2=0
FilterATR,3=0
iCCI_OpenFilter=${iCCI_OpenFilter}
iCCI_OpenFilter,F=0
iCCI_OpenFilter,1=${iCCI_OpenFilter}
iCCI_OpenFilter,2=0.00000000
iCCI_OpenFilter,3=0.00000000
_OpenOrderFilters=---
iMA_Filter_Open_a=${iMA_Filter_Open_a}
iMA_Filter_Open_a,F=0
iMA_Filter_Open_a,1=${iMA_Filter_Open_a}
iMA_Filter_Open_a,2=0
iMA_Filter_Open_a,3=0
iMA_Filter_Open_b=${iMA_Filter_Open_b}
iMA_Filter_Open_b,F=0
iMA_Filter_Open_b,1=${iMA_Filter_Open_b}
iMA_Filter_Open_b,2=0
iMA_Filter_Open_b,3=0
iWPR_Filter_Open_a=${iWPR_Filter_Open_a}
iWPR_Filter_Open_a,F=0
iWPR_Filter_Open_a,1=${iWPR_Filter_Open_a}
iWPR_Filter_Open_a,2=0
iWPR_Filter_Open_a,3=0
iWPR_Filter_Open_b=${iWPR_Filter_Open_b}
iWPR_Filter_Open_b,F=0
iWPR_Filter_Open_b,1=${iWPR_Filter_Open_b}
iWPR_Filter_Open_b,2=0
iWPR_Filter_Open_b,3=0
_CloseOrderFilters=---
Price_Filter_Close=${Price_Filter_Close}
Price_Filter_Close,F=0
Price_Filter_Close,1=${Price_Filter_Close}
Price_Filter_Close,2=0
Price_Filter_Close,3=0
iWPR_Filter_Close=${iWPR_Filter_Close}
iWPR_Filter_Close,F=0
iWPR_Filter_Close,1=${iWPR_Filter_Close}
iWPR_Filter_Close,2=0
iWPR_Filter_Close,3=0
_Add=Расширенные настройки
LongTrade=1
LongTrade,F=0
LongTrade,1=0
LongTrade,2=1
LongTrade,3=1
ShortTrade=1
ShortTrade,F=0
ShortTrade,1=0
ShortTrade,2=1
ShortTrade,3=1
No_Hedge_Trades=1
No_Hedge_Trades,F=0
No_Hedge_Trades,1=0
No_Hedge_Trades,2=1
No_Hedge_Trades,3=1
OneOrderInBarMode=1
OneOrderInBarMode,F=0
OneOrderInBarMode,1=0
OneOrderInBarMode,2=1
OneOrderInBarMode,3=1
MagicNumber=777
MagicNumber,F=0
MagicNumber,1=777
MagicNumber,2=0
MagicNumber,3=0
MaxSpread=2.00000000
MaxSpread,F=0
MaxSpread,1=2.00000000
MaxSpread,2=0.00000000
MaxSpread,3=0.00000000
OpenSlippage=2.00000000
OpenSlippage,F=0
OpenSlippage,1=2.00000000
OpenSlippage,2=0.00000000
OpenSlippage,3=0.00000000
CloseSlippage=3.00000000
CloseSlippage,F=0
CloseSlippage,1=3.00000000
CloseSlippage,2=0.00000000
CloseSlippage,3=0.00000000
RequoteAttempts=3
RequoteAttempts,F=0
RequoteAttempts,1=3
RequoteAttempts,2=0
RequoteAttempts,3=0
WriteLog=1
WriteLog,F=0
WriteLog,1=0
WriteLog,2=1
WriteLog,3=1
WriteDebugLog=1
WriteDebugLog,F=0
WriteDebugLog,1=0
WriteDebugLog,2=1
WriteDebugLog,3=1
PrintLogOnChart=1
PrintLogOnChart,F=0
PrintLogOnChart,1=0
PrintLogOnChart,2=1
PrintLogOnChart,3=1
''')


RUNNER_FOLDER = "tester\\pyRunner"
RUNNER_FOLDER_FOR_SET = RUNNER_FOLDER.replace("tester\\", "")