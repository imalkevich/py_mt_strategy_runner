
select * from dbo.wsrt_configuration
select * from dbo.wsrt_configuration_option where ConfigurationId = 5
select * from dbo.wsrt_run
select * from dbo.wsrt_run_result where RunId = 109
select * from dbo.wsrt_run_result_trade where ResultId = 49110 order by CloseTime ASC

update dbo.wsrt_configuration set [Description] = 'List of configurations - first look at data' where ConfigurationId = 1

--'List of configurations - first look at data'

delete from dbo.wsrt_run where ConfigurationId = 3
delete from wsrt_configuration_option where OptionId > 1605
delete from dbo.wsrt_run_result where ResultId > 47538

UPDATE dbo.wsrt_run_result 
set
	RunStartDateTimeUtc = null
Where 
	ResultId = 49123

INSERT INTO dbo.wsrt_configuration ([Name], [Description])
	VALUES ('2018_deep_learn_test', '2018 deep learning test - moving average period from 50 to 251, step 10, from Jan 2008 - May 2018');

INSERT INTO dbo.wsrt_run ([Name], [TestSymbol], [TestDateFrom], [TestDateTo], [Description], [ConfigurationId])
	VALUES
		('GBPUSD_01012008_06012018_LSTM_history_test', 'GBPUSD', '2008.01.01', '2018.05.01', 'GBPUSD for Jan 2016 - May 2018', 5);

INSERT INTO dbo.wsrt_run_result ([RunId], [OptionId])
	SELECT 1, OptionId FROM dbo.wsrt_configuration_option

declare @runId int = 110
declare @runIdTo int = 110
declare @configurationId int = 5

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


select
	rr.RunId,
	rrt.ResultId, 
	COUNT(rrt.ResultId) as NumTrades,
	Max(rrt.CloseTime) as MaxCloseTime
from 
	dbo.wsrt_run_result_trade rrt
inner join dbo.wsrt_run_result rr on rrt.ResultId = rr.ResultId
where rr.RunId in (select r.RunId from dbo.wsrt_run r where r.ConfigurationId = 4)
group by rr.RunId, rrt.ResultId
order by rrt.ResultId

select * from dbo.wsrt_run_result_trade where ResultId = 49129

delete from dbo.wsrt_run_result_trade where ResultId = 49130 and CloseTime > '2018-04-24 18:20:00.0000000'

