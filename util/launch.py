""" create launch file for MT4 """

import os
from string import Template
from .params import RUNNER_FOLDER
from .report import report_file_folder, report_file_name_template

ini_Template = Template('''; start strategy tester 
TestExpert=wsrt_3.8.5 
TestExpertParameters=${TestExpertParameters}
TestSymbol=${TestSymbol}
TestPeriod=M15
TestModel=0 
TestSpread=2 
TestOptimization=false 
TestDateEnable=true 
TestFromDate=${TestFromDate}
TestToDate=${TestToDate}
TestReport=${TestReport} 
TestReplaceReport=true 
TestShutdownTerminal=true
TestVisualEnable=false
''')

ini_file_folder = "launch"
ini_file_name_template = "{}\\{}\\{}.ini"

def create_ini_file(mt4folder, idx, test_date_from, test_date_to, test_symbol, test_set_file_name):
    f_name = ini_file_name_template.format(RUNNER_FOLDER, ini_file_folder, idx)
    ini_file_name = os.path.join(mt4folder, f_name)

    params = {
        "TestExpertParameters": test_set_file_name,
        "TestSymbol": test_symbol,
        "TestFromDate": test_date_from,
        "TestToDate": test_date_to,
        "TestReport": report_file_name_template.format(RUNNER_FOLDER, report_file_folder, idx)
    }

    ini_file_content = ini_Template.substitute(params)

    os.makedirs(os.path.dirname(ini_file_name), exist_ok=True)
    with open(ini_file_name, "w") as text_file:
        text_file.write(ini_file_content)

    return ini_file_name






