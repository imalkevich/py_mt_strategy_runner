""" configuration run result """

from datetime import datetime
from decimal import Decimal
from .connection import get_connection

_cnxn = get_connection()

def insert(result):
    cursor = _cnxn.cursor()

    with cursor.execute("""
        INSERT INTO [dbo].[wsrt_run_result]
        (
            [TotalNetProfit],
            [GrossProfit],
            [GrossLoss],
            [ProfitFactor],
            [ExpectedPayoff],
            [AbsoluteDrawdown],
            [MaximalDrawdown],
            [RelativeDrawdown],
            [TotalTrades],

            [RunFinishDateTimeUtc]
        )
        VALUES
        (
            ?,?,?,?,?,?,?,?,?,?
        )
    """,
        result[''],
        result[''],
        result[''],
        result[''],
        result[''],
        result[''],
        result[''],
        result[''],
        result[''],
        datetime.utcnow()):
        pass

    _cnxn.commit()

def mark_as_processing(id):
    cursor = _cnxn.cursor()
    tsql = "UPDATE [dbo].[wsrt_run_result] SET [RunStartDateTimeUtc] = ? WHERE [ResultId] = ?"
    with cursor.execute(tsql, datetime.utcnow(), id):
        pass

    _cnxn.commit()

def get_for_processing_by_run_id(run_id):
    run_result = None
    cursor = _cnxn.cursor()
    tsql = """
    SELECT TOP 1
        [ResultId],
        [RunId],
        [OptionId]
    FROM
        [dbo].[wsrt_run_result]
    WHERE
        [RunId] = ?
        AND [RunStartDateTimeUtc] IS NULL
    """
    with cursor.execute(tsql, run_id):
        row = cursor.fetchone()
        if row:
            run_result = dict(zip([column[0] for column in cursor.description], row))
            if run_result:
                # mark result as being processed, so other terminals not to pick it
                process_tsql = """
                    UPDATE [dbo].[wsrt_run_result] SET [RunStartDateTimeUtc] = ?
                    WHERE [ResultId] = ?
                """
                with cursor.execute(process_tsql, datetime.utcnow(), run_result['ResultId']):
                    _cnxn.commit()

    return run_result

def update_run_result_with_report(report):
    """ """
    cursor = _cnxn.cursor()
    tsql = """
    UPDATE [dbo].[wsrt_run_result] SET
        [TotalNetProfit] = ?,
        [GrossProfit] = ?,
        [GrossLoss] = ?,
        [ProfitFactor] = ?,
        [ExpectedPayoff] = ?,
        [AbsoluteDrawdown] = ?,
        [MaximalDrawdown] = ?,
        [TotalTrades] = ?,
        [RunFinishDateTimeUtc] = ?
    WHERE
        [ResultId] = ?
    """
    cursor.execute(tsql,
                    Decimal(report['TotalNetProfit']) if report['TotalNetProfit'] is not None else None,
                    Decimal(report['GrossProfit']) if report['GrossProfit'] is not None else None,
                    Decimal(report['GrossLoss']) if report['GrossLoss'] is not None else None,
                    Decimal(report['ProfitFactor']) if report['ProfitFactor'] is not None else None,
                    Decimal(report['ExpectedPayoff']) if report['ExpectedPayoff'] is not None else None,
                    Decimal(report['AbsoluteDrawdown']) if report['AbsoluteDrawdown'] is not None else None,
                    Decimal(report['MaximalDrawdown']) if report['MaximalDrawdown'] is not None else None,
                    int(report['TotalTrades']) if report['TotalTrades'] is not None else None,
                    datetime.utcnow(),
                    report['ResultId'])

    for trade in report['Trades']:
        add_run_result_trade(cursor, report['ResultId'], trade)

    cursor.close()
    del cursor
    _cnxn.commit()

def add_run_result_trade(cursor, result_id, trade):
    tsql = """
    INSERT INTO [dbo].[wsrt_run_result_trade]
    (
        [ResultId],
        [CloseTime],
        [Profit]
    )
    VALUES
    (
        ?,?,?
    )
    """

    cursor.execute(tsql, result_id, trade['Time'], trade['Profit'])
