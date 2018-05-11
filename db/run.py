""" run """

from .connection import get_connection

def get_by_name(name):
    run = None
    with get_connection() as cnxn:
        cursor = cnxn.cursor()
        tsql = "SELECT * FROM [dbo].[wsrt_run] WHERE Name = ?"
        with cursor.execute(tsql, name):
            row = cursor.fetchone()
            if row:
                run = dict(zip([column[0] for column in cursor.description], row))

    return run

def get_by_configuration_id(config_id):
    runs = list()
    with get_connection() as cnxn:
        cursor = cnxn.cursor()
        tsql = "SELECT * FROM [dbo].[wsrt_run] WHERE ConfigurationId = ? ORDER BY RunId"
        with cursor.execute(tsql, config_id):
            rows = cursor.fetchall()
            for row in rows:
                run = dict(zip([column[0] for column in cursor.description], row))
                runs.append(run)

    return runs
