""" collect results """ 

import os
from datetime import datetime
from util.terminal import TERMINAL_POOL
from util.result_extractor import prepare_results

RESULTS_FILE_NAME = "./output/wsrt_results.csv"

try:
    os.remove(RESULTS_FILE_NAME)
except OSError:
    pass

start_run = datetime.now()
print("start collecting results {} ...".format(datetime.strftime(start_run, "%b %d %y %H:%M:%S %Z")))

prepare_results(RESULTS_FILE_NAME, TERMINAL_POOL)
#prepare_results(RESULTS_FILE_NAME, ["d:\\Program Files\\GAINSY MT4"])

finish_run = datetime.now()
print("end collecting results {} ...".format(datetime.strftime(finish_run, "%b %d %y %H:%M:%S %Z")))

input("press Enter to exit ...")


