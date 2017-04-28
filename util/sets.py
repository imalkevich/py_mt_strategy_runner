""" create launch file for MT4 """

import os
from .params import set_Template, RUNNER_FOLDER, RUNNER_FOLDER_FOR_SET

set_file_folder = "sets"
set_file_name_template = "{}\\{}\\{}.set"
set_file_name_template_for_ini_file = "{}\\{}\\{}.set"

def create_set_file(mt4folder, configuration, idx):
    set_file_name = os.path.join(mt4folder, set_file_name_template.format(RUNNER_FOLDER, set_file_folder, idx))

    set_file_content = set_Template.substitute(configuration)

    with open(set_file_name, "w") as text_file:
        text_file.write(set_file_content)

    return set_file_name_template_for_ini_file.format(RUNNER_FOLDER_FOR_SET, set_file_folder, idx)






