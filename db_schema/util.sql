-- 
INSERT INTO dbo.wsrt_configuration ([Name], [Description])
	VALUES ('iMA_Period_50_251', 'iMA_Period_50_251 configuration - moving average period from 50 to 251, step 1');

-- Create entry for wsrt_run
INSERT INTO dbo.wsrt_run ([Name], [TestSymbol], [TestDateFrom], [TestDateTo], [Description], [ConfigurationId])
	VALUES
		('GBPUSD_05012017_06012017_IMAPeriod', 'GBPUSD', '2017.05.01', '2010.06.01', 'GBPUSD for May 2017', 2);

-- create new run results from configuration
INSERT INTO dbo.wsrt_run_result ([RunId], [OptionId])
	SELECT 1, OptionId FROM dbo.wsrt_configuration_option

-- incremental insert
declare @runId int = 17
declare @runIdTo int = 106
declare @configurationId int = 2

WHILE @runId <= @runIdTo
BEGIN
	
	INSERT INTO dbo.wsrt_run_result ([RunId], [OptionId])
		SELECT @runId, OptionId FROM dbo.wsrt_configuration_option
			WHERE
				ConfigurationId = @configurationId 
				AND OptionId NOT IN (SELECT OptionId FROM dbo.wsrt_run_result WHERE RunId = @runId)
	
	--select count(1) from dbo.wsrt_run_result where RunId = @runId
	SELECT @runId = @runId + 1;
END