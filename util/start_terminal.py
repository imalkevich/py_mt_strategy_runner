""" code for init terminal """
import os
import shutil

from .params import RUNNER_FOLDER

from .launch import ini_file_folder
from .sets import set_file_folder
from .report import report_file_folder

def init_terminal(terminal_path):
    """ """
    # remove directory before start to avoid pollution
    if os.path.isdir(os.path.join(terminal_path, RUNNER_FOLDER)):
        shutil.rmtree(os.path.join(terminal_path, RUNNER_FOLDER))

    os.makedirs(os.path.join(terminal_path, RUNNER_FOLDER), exist_ok=True)
    os.makedirs(os.path.join(terminal_path, RUNNER_FOLDER, ini_file_folder), exist_ok=True)
    os.makedirs(os.path.join(terminal_path, RUNNER_FOLDER, set_file_folder), exist_ok=True)
    os.makedirs(os.path.join(terminal_path, RUNNER_FOLDER, report_file_folder), exist_ok=True)
