""" configuration run result """

import pandas

from datetime import datetime
from decimal import Decimal
from .connection import get_connection

_cnxn = get_connection()

def _get_connection():
    return _cnxn

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

def get_completed_run_results_by_configuration_id(configuration_id):
    tsql = """
    SELECT rr.* from dbo.wsrt_run_result rr
    WHERE
        rr.RunId 
        IN (SELECT r.RunId FROM dbo.wsrt_run r WHERE r.ConfigurationId = ?)
        AND rr.RunFinishDateTimeUtc IS NOT NULL
    """
    cnxn = _get_connection()
    cursor = cnxn.cursor()
    cursor.execute(tsql, configuration_id)

    rows = [dict(zip([column[0] for column in cursor.description], row)) for row in cursor.fetchall()]

    cursor.close()
    del cursor

    return rows

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

def get_run_result_trades_by_result_id(result_id):
    tsql = """
    SELECT 
        rrt.* 
    FROM 
        dbo.wsrt_run_result_trade rrt
    WHERE
        rrt.ResultId = ?
    ORDER BY
        rrt.CloseTime ASC
    """
    cnxn = _get_connection()
    cursor = cnxn.cursor()
    cursor.execute(tsql, result_id)

    rows = [dict(zip([column[0] for column in cursor.description], row)) for row in cursor.fetchall()]
    df = pandas.DataFrame(rows)

    cursor.close()
    del cursor

    return df

def remove_run_result_trades_by_configuration_id(configuration_id):
    tsql = """
    DELETE FROM dbo.wsrt_run_result_trade
    WHERE [ResultId] IN 
        (SELECT rr.[ResultId] FROM dbo.wsrt_run_result rr WHERE rr.[RunId] IN
            (SELECT r.[RunId] FROM dbo.wsrt_run r WHERE r.[ConfigurationId] = ?)
        )
    """
    cnxn = _get_connection()
    cursor = cnxn.cursor()

    cursor.execute(tsql, configuration_id)

    cursor.close()
    del cursor
    cnxn.commit()

def reset_run_results_by_configuration_id(configuration_id):
    tsql = """
    UPDATE 
        dbo.wsrt_run_result
    SET
        [RunStartDateTimeUtc] = NULL
    WHERE 
        [RunId] IN 
        (SELECT r.[RunId] FROM dbo.wsrt_run r WHERE r.[ConfigurationId] = ?)
    """
    cnxn = _get_connection()
    cursor = cnxn.cursor()

    cursor.execute(tsql, configuration_id)

    cursor.close()
    del cursor
    cnxn.commit()

def get_run_result_trades_summary_by_configuration_id(configuration_id):
    tsql = """
    select
        rr.RunId,
        rrt.ResultId, 
        COUNT(rrt.ResultId) as NumTrades,
        Max(rrt.CloseTime) as MaxCloseTime
    from 
        dbo.wsrt_run_result_trade rrt
    inner join dbo.wsrt_run_result rr on rrt.ResultId = rr.ResultId
    where rr.RunId in (select r.RunId from dbo.wsrt_run r where r.ConfigurationId = ?)
    group by rr.RunId, rrt.ResultId
    order by rrt.ResultId
    """
    cnxn = _get_connection()
    cursor = cnxn.cursor()
    cursor.execute(tsql, configuration_id)

    rows = [dict(zip([column[0] for column in cursor.description], row)) for row in cursor.fetchall()]
    df = pandas.DataFrame(rows)

    cursor.close()
    del cursor

    return df

def delete_trades_by_rusult_id_and_close_time(result_id, cutoff_close_time):
    tsql = '''
        delete from dbo.wsrt_run_result_trade where ResultId = ? and CloseTime > ?
    '''
    cnxn = _get_connection()
    cursor = cnxn.cursor()

    cursor.execute(tsql, result_id, cutoff_close_time)

    cursor.close()
    del cursor
    cnxn.commit()