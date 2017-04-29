-- Create entry for wsrt_run
INSERT INTO dbo.wsrt_run ([Name], [TestSymbol], [TestDateFrom], [TestDateTo], [Description])
	VALUES
		('GBPUSD_03012017_04012017', 'GBPUSD', '2017.03.01', '2017.04.01', 'GBPUSD for March 2017')

-- create new run results from configuration
INSERT INTO dbo.wsrt_run_result ([RunId], [OptionId])
	SELECT 1, OptionId FROM dbo.wsrt_configuration_option