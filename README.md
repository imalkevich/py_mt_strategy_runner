This is an utility to collect MT4 experts reports.

The idea is:
1) Create .set file with expert configuration to be used for emulation;
2) Create .ini file with MT4 remote start with preselected *.set file from set 1;
3) Run the script with the following args - symbol dateFrom dateTo, for example "main.py GBPUSD 2017.03.01 2017.04.01".

Think about the following:
1) Separate step with getting configuration and running MT4 workers;
2) Use database for storing configurations;
3) Use database for processing configurations while running MT4 agents.