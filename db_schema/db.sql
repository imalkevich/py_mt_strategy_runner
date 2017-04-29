CREATE TABLE [dbo].[wsrt_configuration_option] (
    [OptionId] INT IDENTITY (1, 1) NOT NULL,
	
	[TakeProfit] INT NOT NULL,
	[StopLoss] INT NOT NULL,
	[UseStopLevels] BIT NOT NULL,
	[SecureProfit] INT NOT NULL,
	[SecureProfitTriger] INT NOT NULL,
	[MaxLossPoints] INT NOT NULL,
	[RecoveryMode] BIT NOT NULL,
	[FixedLot] DECIMAL(5,1) NOT NULL,
	[AutoMM] DECIMAL(5,1) NOT NULL,
	[AutoMM_Max] DECIMAL(5,1) NOT NULL,
	[Risk] DECIMAL(5,1) NOT NULL,
	[MultiLotPercent] DECIMAL(5,1) NOT NULL,

	[iMA_Period] INT NOT NULL,
	[iCCI_Period] INT NOT NULL,
	[iATR_Period] INT NOT NULL,
	[iWPR_Period] INT NOT NULL,

	[FilterATR] INT NOT NULL,
	[iCCI_OpenFilter] DECIMAL(5,1) NOT NULL,

	[iMA_Filter_Open_a] INT NOT NULL,
	[iMA_Filter_Open_b] INT NOT NULL,
	[iWPR_Filter_Open_a] INT NOT NULL,
	[iWPR_Filter_Open_b] INT NOT NULL,

	[Price_Filter_Close] INT NOT NULL,
	[iWPR_Filter_Close] INT NOT NULL,

    [CreatedDateTimeUtc] DATETIME2 (7)  CONSTRAINT [DF_wsrt_configuration_option_CreatedDateTimeUtc] DEFAULT (sysutcdatetime()) NOT NULL,
    
	CONSTRAINT [PK_wsrt_configuration_option] PRIMARY KEY CLUSTERED ([OptionId] ASC)
);

CREATE TABLE [dbo].[wsrt_run] (
	[RunId] INT IDENTITY (1, 1) NOT NULL,
	[Name] NVARCHAR(256) NOT NULL,
	[TestSymbol] VARCHAR(32) NOT NULL,
	[TestDateFrom] VARCHAR(32) NOT NULL, 
	[TestDateTo] VARCHAR(32) NOT NULL,
	[Description] NVARCHAR(MAX) NULL,

	[CreatedDateTimeUtc] DATETIME2 (7)  CONSTRAINT [DF_wsrt_run_CreatedDateTimeUtc] DEFAULT (sysutcdatetime()) NOT NULL,

	CONSTRAINT [PK_wsrt_run] PRIMARY KEY CLUSTERED ([RunId] ASC)
);

ALTER TABLE [dbo].[wsrt_run]
	ADD CONSTRAINT [U_wsrt_run_name] UNIQUE ([Name]);

--DROP TABLE [dbo].[wsrt_run_result]
CREATE TABLE [dbo].[wsrt_run_result](
	[ResultId] INT IDENTITY (1, 1) NOT NULL,
	[RunId] INT NOT NULL,
	[OptionId] INT NOT NULL,

	[TotalNetProfit] DECIMAL(10,2) NULL,
	[GrossProfit] DECIMAL(10,2) NULL,
	[GrossLoss] DECIMAL(10,2) NULL,
	[ProfitFactor] DECIMAL(10,2) NULL,
	[ExpectedPayoff] DECIMAL(10,2) NULL,
	[AbsoluteDrawdown] DECIMAL(10,2) NULL,
	[MaximalDrawdown] DECIMAL(10,2) NULL,
	[TotalTrades] INT NULL,

	[RunStartDateTimeUtc] DATETIME2 (7) NULL,
	[RunFinishDateTimeUtc] DATETIME2 (7) NULL, 

	CONSTRAINT [PK_wsrt_run_result] PRIMARY KEY CLUSTERED ([ResultId] ASC),
	CONSTRAINT [FK_run_result_run] FOREIGN KEY ([RunId]) REFERENCES [dbo].[wsrt_run] ([RunId]) ON DELETE CASCADE,
	CONSTRAINT [FK_run_result_configuration_option] FOREIGN KEY ([OptionId]) REFERENCES [dbo].[wsrt_configuration_option] ([OptionId]) ON DELETE CASCADE
);