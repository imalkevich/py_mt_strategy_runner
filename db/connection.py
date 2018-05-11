""" configuration """

import sys
import pyodbc

from datetime import datetime, timedelta

from util.config import config
from util.logging import print_now

def get_connection():
    """ get connection """
    server = config.get('mssql', 'server')
    database = config.get('mssql', 'database')
    username = config.get('mssql', 'username')
    password = config.get('mssql', 'password')
    driver= '{ODBC Driver 13 for SQL Server}'
    
    cnxn = None
    attempts = 0
    start_run_time = datetime.now()

    while cnxn is None:
        try:
            cnxn = pyodbc.connect('DRIVER='+driver+';PORT=1433;SERVER='+server+';PORT=1443;DATABASE='+database+';UID='+username+';PWD='+password)
        except:
            attempts += 1
            if attempts % 10:
                print_now('Unable to open database connection...')

    if attempts > 0:
        print_now('Opening database connection took {}'.format(datetime.now() - start_run_time))

    return cnxn








