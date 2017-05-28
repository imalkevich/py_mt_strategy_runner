select * from wsrt_configuration
select * from wsrt_configuration_option where ConfigurationId = 2

select * from wsrt_run
update wsrt_run set [TestDateTo] = '2017.06.01' where RunId=106
select count(1) from wsrt_run_result where RunFinishDateTimeUtc is not null
select count(1) from wsrt_run_result where RunFinishDateTimeUtc is null
select count(1) from wsrt_run_result where RunId = 17 and RunFinishDateTimeUtc is null
select * from wsrt_run_result where RunId = 106 and RunFinishDateTimeUtc is not null 

select * from wsrt_run_result where RunStartDateTimeUtc is not null and RunFinishDateTimeUtc IS NULL
update wsrt_run_result set RunStartDateTimeUtc = NULL WHERE RunStartDateTimeUtc is not null and RunFinishDateTimeUtc IS NULL
--update wsrt_run_result set RunStartDateTimeUtc = NULL WHERE ResultId >= 47285 and ResultId <= 47288
--delete wsrt_run_result where ResultId >= 38879 and ResultId <= 38886
--delete from wsrt_configuration_option where OptionId > 73
--delete from wsrt_run_result where ResultId >= 34971
--delete from wsrt_configuration_option

select
	AVG(DATEDIFF(SECOND, RunFinishDateTimeUtc, RunStartDateTimeUtc))
	--DATEDIFF(SECOND, RunFinishDateTimeUtc, RunStartDateTimeUtc)
from wsrt_run_result
where 
	RunFinishDateTimeUtc is not null
	and RunId = 92

select * from wsrt_run
select
	rr.TotalNetProfit as TotalNetProfit,
	rr.AbsoluteDrawdown,
	rr.MaximalDrawdown,
	rr.TotalTrades as TotalTrades,

	op.TakeProfit as TakeProfit,
	op.StopLoss as StopLoss,
	op.UseStopLevels as UseStopLevels,
	op.SecureProfit as SecureProfit,
	op.SecureProfitTriger as SecureProfitTriger,
	op.MaxLossPoints as MaxLossPoints,
	op.RecoveryMode as RecoveryMode,
	op.FixedLot as FixedLot,
	op.AutoMM as AutoMM,
	op.AutoMM_Max as AutoMM_Max,
	op.Risk as Risk,
	op.MultiLotPercent as MultiLotPercent,
	op.iMA_Period as iMA_Period,
	op.iCCI_Period as iCCI_Period,
	op.iATR_Period as iATR_Period,
	op.iWPR_Period as iWPR_Period,
	op.FilterATR as FilterATR,
	op.iCCI_OpenFilter as iCCI_OpenFilter,
	op.iMA_Filter_Open_a as iMA_Filter_Open_a,
	op.iMA_Filter_Open_b as iMA_Filter_Open_b,
	op.iWPR_Filter_Open_a as iWPR_Filter_Open_a,
	op.iWPR_Filter_Open_b as iWPR_Filter_Open_b,
	op.Price_Filter_Close as Price_Filter_Close,
	op.iWPR_Filter_Close as iWPR_Filter_Close
from
	wsrt_run_result rr
	inner join wsrt_configuration_option op on rr.OptionId = op.OptionId
where
	rr.RunFinishDateTimeUtc IS NOT NULL
	and rr.RunId = 20
order by 
	op.iMA_Period
