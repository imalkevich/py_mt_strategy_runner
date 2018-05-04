""" """

import pandas as pd

from datetime import datetime, timedelta

from .config import config

from . import terminal

TERMINAL_POOL = []

if config.has_section("terminal"):
    TERMINAL_POOL = [{'exe_path': t[0], 'data_path': t[1] } for t in [t.split('|') for t in config.get("terminal", "pool").split(",")]]

DATE_FORMAT = '%Y.%m.%d'

def get_run_result_date_from(run_date_from, run_result_id, df_run_trades, shift_days=1):
    run_date_from = datetime.strptime(run_date_from, DATE_FORMAT)

    if df_run_trades is not None and df_run_trades.shape[0] > 0:
        filtered = df_run_trades[df_run_trades['ResultId'] == run_result_id]
        max_close_time = pd.to_datetime(filtered['MaxCloseTime'].values[0])

        max_close_time = max_close_time - timedelta(days=shift_days)
        if shift_days > 0:
            max_close_time = datetime(max_close_time.year, max_close_time.month, max_close_time.day)
        else:
            max_close_time = datetime(max_close_time.year, max_close_time.month, max_close_time.day, max_close_time.hour, max_close_time.minute)

        if max_close_time > run_date_from:
            run_date_from = max_close_time

    return run_date_from

def get_run_result_date_from_formatted(run_date_from, run_result_id, df_run_trades):
    run_date_from = terminal.get_run_result_date_from(run_date_from, run_result_id, df_run_trades)

    formatted = '{}'.format(run_date_from.strftime(DATE_FORMAT))

    return formatted