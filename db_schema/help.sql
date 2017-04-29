

select * from wsrt_configuration_option
select * from wsrt_run
select * from wsrt_run_result

update wsrt_run_result set RunStartDateTimeUtc = NULL
delete from wsrt_run_result where ResultId > 1

select
	AVG(DATEDIFF(SECOND, RunFinishDateTimeUtc, RunStartDateTimeUtc))
	--DATEDIFF(SECOND, RunFinishDateTimeUtc, RunStartDateTimeUtc)
from wsrt_run_result