py_mt_strategy_runner
====================================================

command line utility to collect MT4 experts reports.
-------------------------------------------

.. image:: https://secure.travis-ci.org/imalkevich/py_mt_strategy_runner.png?branch=master
        :target: https://travis-ci.org/imalkevich/py_mt_strategy_runner

.. image:: https://codecov.io/github/imalkevich/py_mt_strategy_runner/coverage.svg?branch=master
    :target: https://codecov.io/github/imalkevich/py_mt_strategy_runner
    :alt: codecov.io

Idea
----

1) Create configuration in dbo.wsrt_configuration:
    INSERT INTO dbo.wsrt_configuration ([Name], [Description])
	    VALUES ('{Configuration name}', '{Description}');

2) Prepare configurations:
    - Open ./util/params.py file and edit 'param_grid' with needed ranges;
    - Run ./prepare_configuration.py from cmd, like:
        "python prepare_configuration.py iMA_Period_50_251", where iMA_Period_50_251 is configuration name (entry from step #1 above)

2) Create a run - entry in wsrt_run table (if not exists) by running the following SQL:
    INSERT INTO dbo.wsrt_run ([Name], [TestSymbol], [TestDateFrom], [TestDateTo], [Description], [ConfigurationId])
	VALUES
		('GBPUSD_05012017_06012017_IMAPeriod', 'GBPUSD', '2017.05.01', '2017.06.01', 'GBPUSD for May 2017', 2);
    
3) Insert new dbo.wsrt_run_result by running (take @runId from step #2):
    -- incremental insert
    declare @runId int = 17
    declare @runIdTo int = 105
    declare @configurationId int = 2

    WHILE @runId <= @runIdTo
    BEGIN
        INSERT INTO dbo.wsrt_run_result ([RunId], [OptionId])
            SELECT @runId, OptionId FROM dbo.wsrt_configuration_option
                WHERE
                    ConfigurationId = @configurationId 
                    AND OptionId NOT IN (SELECT OptionId FROM dbo.wsrt_run_result WHERE RunId = @runId)
        -- check the amount of all configurations
        -- select count(1) from dbo.wsrt_run_result where RunId = @runId
        SELECT @runId = @runId + 1;
    END

4) Make sure config.yaml has database connection string and terminals, like:
    ; configuration
    [mssql]
    server = {database_server}
    database = {database_name}
    username  = {user_name}
    password = {password}

    [terminal]
    pool = {exe file folder}|{data path folder}

5) Run main script to collect MT4 results and store them into database:
    "python main.py {configurationId} [refresh]"
    
    Where configurationId from step #1, 'refresh' is optional (if exists will delede related records from 
    wsrt_run_result_trade, and update wsrt_run_result.RunStartDateTimeUtc to NULL)

6) Run the following command to perform analysis and predictions for a configuration:
    python -m machine_learning.analytics
    usage: analytics.py [-h] [-cid CONFIGURATION_ID] [-v]

    predict future trades of different configuration options

    optional arguments:
    -h, --help            show this help message and exit
    -cid CONFIGURATION_ID, --configuration_id CONFIGURATION_ID
                            configuration id
    -v, --version         displays the current version of analytics module


Run terminals to collect reports:
Installing Microsoft ODBC Driver 13.1 might be required (https://www.microsoft.com/download/details.aspx?id=53339). 
Also install pyodbc module for python (pip install pyodbc)

How to create environment:
>> cd py_mt_strategy_runner
>> virtualenv --python python venv
>> source venv/Scripts/activate

How it works internally:
1) List of configurations is stored in dbo.wsrt_configuration;
1) List of available configuration options linked to configuration is stored in dbo.wsrt_configuration_option table
2) List of run is saved in dbo.wsrt_run table;
3) To create a run results, you need to prepare dbo.wsrt_run_result table with needed configurations;
4) Once srcipt is started, it will:
    - Look for a runs by configurationid provided as input
    - Select not run configurations - for those where Run start datetime is NULL
    - Once configuration is run in MT terminal, script will parse report and store it in the database

MT4 details 
The approach for running MT4 is simple:
1) Grab configuration from database and save it in .set file;
2) Create .ini file with MT4 remote start with set file from step #1 above;
3) Remote start of terminal in a separate process with .ini file from step #2;
4) Once the process is finishe, pick report.html file, parse it, send data to database.

Interruption during run:
------------------------

1) As long as script might take a long time to run (days), it is nesessary to make the
whole approach tolerant for such interruptions;
2) The script is design with this in mind, so whenever you need to stop it - close the window, and that should be it;
3) Once you are at the point where you are coming to the end of collection data, 
please make sure that there are no entries for dbo.wsrt_run_result with Run start datetime not NULL, but Finish datetime is NULL. 
This means that during running you had to stop script execution, and some processes running at that point didn't have a chance to complete.