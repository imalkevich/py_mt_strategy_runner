""" configuration option """

import pyodbc
from .connection import get_connection

def get_configurations_count():
    with get_connection() as cnxn:
        cursor = cnxn.cursor()
        with cursor.execute("SELECT COUNT(1) from [dbo].[wsrt_configuration_option]"):
            (number_of_rows,)=cursor.fetchone()

        cursor.close()
        del cursor
    
    return number_of_rows

def get_option_by_id(id):
    option = None
    with get_connection() as cnxn:
        cursor = cnxn.cursor()
        with cursor.execute("""
            SELECT * FROM [dbo].[wsrt_configuration_option] WHERE [OptionId] = ?
            """, id):
            option = dict(zip([column[0] for column in cursor.description], cursor.fetchone()))

    return option

def insert_configuration(opt, configurationId):
    with get_connection() as cnxn:
        cursor = cnxn.cursor()
        try:
            with cursor.execute("""INSERT INTO [dbo].[wsrt_configuration_option]
                (
                    TakeProfit, 
                    StopLoss, 
                    UseStopLevels, 
                    SecureProfit, 
                    SecureProfitTriger,
                    MaxLossPoints,
                    RecoveryMode,
                    FixedLot,
                    AutoMM,
                    AutoMM_Max,
                    Risk,
                    MultiLotPercent,

                    iMA_Period,
                    iCCI_Period,
                    iATR_Period,
                    iWPR_Period,

                    FilterATR,
                    iCCI_OpenFilter,

                    iMA_Filter_Open_a,
                    iMA_Filter_Open_b,
                    iWPR_Filter_Open_a,
                    iWPR_Filter_Open_b,

                    Price_Filter_Close,
                    iWPR_Filter_Close,

                    ConfigurationId
                ) 
                VALUES 
                (
                    ?,?,?,?,?,?,?,?,?,?,?,?,
                    ?,?,?,?,?,?,?,?,?,?,?,?,
                    ?
                )
            """,
                                opt['TakeProfit'],
                                opt['StopLoss'],
                                opt['UseStopLevels'],
                                opt['SecureProfit'],
                                opt['SecureProfitTriger'],
                                opt['MaxLossPoints'],
                                opt['RecoveryMode'],
                                opt['FixedLot'],
                                opt['AutoMM'],
                                opt['AutoMM_Max'],
                                opt['Risk'],
                                opt['MultiLotPercent'],

                                opt['iMA_Period'],
                                opt['iCCI_Period'],
                                opt['iATR_Period'],
                                opt['iWPR_Period'],

                                opt['FilterATR'],
                                opt['iCCI_OpenFilter'],

                                opt['iMA_Filter_Open_a'],
                                opt['iMA_Filter_Open_b'],
                                opt['iWPR_Filter_Open_a'],
                                opt['iWPR_Filter_Open_b'],

                                opt['Price_Filter_Close'],
                                opt['iWPR_Filter_Close'],
                                configurationId):
                cnxn.commit()
        except pyodbc.IntegrityError as err:
            print(err)

