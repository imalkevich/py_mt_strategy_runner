-- Create entry for wsrt_run
INSERT INTO dbo.wsrt_run ([Name], [TestSymbol], [TestDateFrom], [TestDateTo], [Description])
	VALUES
		('GBPUSD_04012017_05012017', 'GBPUSD', '2017.04.01', '2017.05.01', 'GBPUSD for April 2017')

-- create new run results from configuration
INSERT INTO dbo.wsrt_run_result ([RunId], [OptionId])
	SELECT 1, OptionId FROM dbo.wsrt_configuration_option

-- incremental insert
INSERT INTO dbo.wsrt_run_result ([RunId], [OptionId])
	SELECT 16, OptionId FROM dbo.wsrt_configuration_option
		WHERE
			OptionId NOT IN (SELECT OptionId FROM dbo.wsrt_run_result WHERE RunId = 16)
