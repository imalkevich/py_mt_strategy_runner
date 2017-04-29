

select * from wsrt_configuration_option
select * from wsrt_run
select * from wsrt_run_result

update wsrt_run_result set RunStartDateTimeUtc = NULL WHERE RunFinishDateTimeUtc IS NULL
delete from wsrt_run_result where ResultId > 1
delete from wsrt_configuration_option

select
	AVG(DATEDIFF(SECOND, RunFinishDateTimeUtc, RunStartDateTimeUtc))
	--DATEDIFF(SECOND, RunFinishDateTimeUtc, RunStartDateTimeUtc)
from wsrt_run_result

select
	rr.TotalNetProfit,

	op.TakeProfit,
	op.StopLoss,
	op.UseStopLevels,
	op.SecureProfit,
	op.SecureProfitTriger,
	op.MaxLossPoints,
	op.RecoveryMode,
	op.FixedLot,
	op.AutoMM,
	op.AutoMM_Max,
	op.Risk,
	op.MultiLotPercent,
	op.iMA_Period,
	op.iCCI_Period,
	op.iATR_Period,
	op.iWPR_Period,
	op.FilterATR,
	op.iCCI_OpenFilter,
	op.iMA_Filter_Open_a,
	op.iMA_Filter_Open_b,
	op.iWPR_Filter_Open_a,
	op.iWPR_Filter_Open_b,
	op.Price_Filter_Close,
	op.iWPR_Filter_Close
from
	wsrt_run_result rr
	inner join wsrt_configuration_option op on rr.OptionId = op.OptionId
where
	rr.RunFinishDateTimeUtc IS NOT NULL