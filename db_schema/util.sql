-- 
INSERT INTO dbo.wsrt_configuration ([Name], [Description])
	VALUES ('iMA_Period_50_251', 'iMA_Period_50_251 configuration - moving average period from 50 to 251, step 1');

-- Create entry for wsrt_run
INSERT INTO dbo.wsrt_run ([Name], [TestSymbol], [TestDateFrom], [TestDateTo], [Description], [ConfigurationId])
	VALUES
		('GBPUSD_01012010_02012011_IMAPeriod', 'GBPUSD', '2010.01.01', '2010.02.01', 'GBPUSD for Jan 2010', 2);

-- create new run results from configuration
INSERT INTO dbo.wsrt_run_result ([RunId], [OptionId])
	SELECT 1, OptionId FROM dbo.wsrt_configuration_option

-- incremental insert
declare @runId int = 71
declare @configurationId int = 2

--WHILE @runId <= 105
--BEGIN
	INSERT INTO dbo.wsrt_run_result ([RunId], [OptionId])
		SELECT @runId, OptionId FROM dbo.wsrt_configuration_option
			WHERE
				ConfigurationId = @configurationId 
				AND OptionId NOT IN (SELECT OptionId FROM dbo.wsrt_run_result WHERE RunId = @runId)
	--SELECT @runId = @runId + 1;
--END