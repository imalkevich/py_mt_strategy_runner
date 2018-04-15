This is an utility to collect MT4 experts reports.

The idea is:
1) Create configuration in dbo.wsrt_configuration;
1) Create configuration options in dbo.wsrt_configuration_option table (if not exists) and link them to dbo.wsrt_configuration;
2) Create a run - entry in wsrt_run table (if not exists);
3) Run terminals for a specific run from step #2 above.

Prepare configurations:
1) Add new entry to dbo.wsrt_configuration
1) Open ./util/params.py file and edit 'param_grid' with needed ranges;
2) Run ./prepare_configuration.py from cmd, like:
    - When in directory, run "python prepare_configuration.py iMA_Period_50_251", where iMA_Period_50_251 is configuration name (entry from step #1 above)

Run terminals to collect reports:
1) Install Microsoft ODBC Driver 13.1 (https://www.microsoft.com/download/details.aspx?id=53339). 
Also install pyodbc module for python (pip install pyodbc)
2) Add new entry/entries to dbo.wsrt_run (connection string is in config.yaml)
    
3) Insert new dbo.wsrt_run_result by running:
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
3) Run script for execution:
    - Run main.py with configuration id, something like:
        "python main.py 2"
    - Wait for the script to complete. As long as it may take long, you might need to
        stop execution. In this case please refer to interruption section below.

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
1) As long as script might take a long time to run (days), it is nesessary to make the
whole approach tolerant for such interruptions;
2) The script is design with this in mind, so whenever you need to stop it - close the window, and that should be it;
3) Once you are at the point where you are coming to the end of collection data, 
please make sure that there are no entries for dbo.wsrt_run_result with Run start datetime not NULL, but Finish datetime is NULL. 
This means that during running you had to stop script execution, and some processes running at that point didn't have a chance to complete.