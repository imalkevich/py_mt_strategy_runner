""" configuration """

import pyodbc
from util.config import config

if config.has_section("mssql"):
    _server = config.get('mssql', 'server')
    _database = config.get('mssql', 'database')
    _username = config.get('mssql', 'username')
    _password = config.get('mssql', 'password')
    _driver= '{ODBC Driver 13 for SQL Server}'
    _cnxn = pyodbc.connect('DRIVER='+_driver+';PORT=1433;SERVER='+_server+';PORT=1443;DATABASE='+_database+';UID='+_username+';PWD='+ _password)

def get_connection():
    """ get connection """
    return _cnxn








