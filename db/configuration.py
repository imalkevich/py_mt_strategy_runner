""" configuration """

import pyodbc
from .connection import get_connection

_cnxn = get_connection()

def get_configuration_by_name(name):
    configuration = None
    cursor = _cnxn.cursor()
    with cursor.execute("""
        SELECT * FROM [dbo].[wsrt_configuration] WHERE [Name] = ?
        """, name):
        configuration = dict(zip([column[0] for column in cursor.description], cursor.fetchone()))

    return configuration