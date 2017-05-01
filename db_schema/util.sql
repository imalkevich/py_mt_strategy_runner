-- Create entry for wsrt_run
INSERT INTO dbo.wsrt_run ([Name], [TestSymbol], [TestDateFrom], [TestDateTo], [Description])
	VALUES
		('GBPUSD_01012016_02012016', 'GBPUSD', '2016.01.01', '2016.02.01', 'GBPUSD for January 2016')

-- create new run results from configuration
INSERT INTO dbo.wsrt_run_result ([RunId], [OptionId])
	SELECT 1, OptionId FROM dbo.wsrt_configuration_option

-- incremental insert
INSERT INTO dbo.wsrt_run_result ([RunId], [OptionId])
	SELECT 15, OptionId FROM dbo.wsrt_configuration_option
		WHERE
			OptionId NOT IN (SELECT OptionId FROM dbo.wsrt_run_result WHERE RunId = 15)
