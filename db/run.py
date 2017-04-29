""" run """

from .connection import get_connection

_cnxn = get_connection()

def get_by_name(name):
    run = None
    cursor = _cnxn.cursor()
    tsql = "SELECT * FROM [dbo].[wsrt_run] WHERE NAME = ?"
    with cursor.execute(tsql, name):
        row = cursor.fetchone()
        if row:
            run = dict(zip([column[0] for column in cursor.description], row))

    return run
