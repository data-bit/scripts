USE [ReportServer]
GO

SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

-- =========================================================
-- Author:		Mitch Alves
-- Description:	Subscriptions Details
-- =========================================================

CREATE VIEW [dbo].[vw_Subscriptions_Details]  AS   

    SELECT
          [Report_Name] =  c.Name
        , [Subscription_Link] = 'http://ssrs.server/Reports/manage/catalogitem/subscriptions/'
			+ ISNULL(REPLACE(( SELECT item FROM dbo.tvf_SplitCustomStrings (Path, '/') WHERE id = 2 ),' ', '%20') + '/', '')
            + ISNULL(REPLACE(( SELECT item FROM dbo.tvf_SplitCustomStrings (Path, '/') WHERE id = 3 ),' ', '%20') + '/', '')
			+ ISNULL(REPLACE(( SELECT item FROM dbo.tvf_SplitCustomStrings (Path, '/') WHERE id = 4 ),' ', '%20') + '/', '')
            + ISNULL(REPLACE(( SELECT item FROM dbo.tvf_SplitCustomStrings (Path, '/') WHERE id = 5 ),' ', '%20') +'/', '')
			+ ISNULL(REPLACE(( SELECT item FROM dbo.tvf_SplitCustomStrings (Path, '/') WHERE id = 6 ),' ', '%20') +'/', '')
        , [Folder_Lv1] = ( SELECT item FROM dbo.tvf_SplitCustomStrings (Path, '/') WHERE id = 2 )
		, [Folder_Lv2] = ( SELECT item FROM dbo.tvf_SplitCustomStrings (Path, '/') WHERE id = 3 )
		, [Folder_Lv3] = ( SELECT item FROM dbo.tvf_SplitCustomStrings (Path, '/') WHERE id = 4 )
        , [Next_Run_Date] = 
			CASE next_run_date WHEN 0 THEN null
				ELSE
				substring(convert(varchar(15),next_run_date),1,4) + '-' +
				substring(convert(varchar(15),next_run_date),5,2) + '-' +
				substring(convert(varchar(15),next_run_date),7,2)
			END +' '+
		/*,[Next Run Time] = */isnull(CASE len(next_run_time)
			WHEN 3 THEN cast('00:0'
			+ Left(right(next_run_time,3),1)
			+':' + right(next_run_time,2) as char (8))
			WHEN 4 THEN cast('00:'
			+ Left(right(next_run_time,4),2)
			+':' + right(next_run_time,2) as char (8))
			WHEN 5 THEN cast('0' + Left(right(next_run_time,5),1)
			+':' + Left(right(next_run_time,4),2)
			+':' + right(next_run_time,2) as char (8))
			WHEN 6 THEN cast(Left(right(next_run_time,6),2)
			+':' + Left(right(next_run_time,4),2)
			+':' + right(next_run_time,2) as char (8))
			END,'NA')
		, [To] = Convert(XML,[ExtensionSettings]).value('(//ParameterValue/Value[../Name="TO"])[1]','nvarchar(150)') 
        , [CC] = Convert(XML,[ExtensionSettings]).value('(//ParameterValue/Value[../Name="CC"])[1]','nvarchar(150)')
        , [Render Format] = Convert(XML,[ExtensionSettings]).value('(//ParameterValue/Value[../Name="RenderFormat"])[1]','nvarchar(150)')
        , [Subject] = Convert(XML,[ExtensionSettings]).value('(//ParameterValue/Value[../Name="Subject"])[1]','nvarchar(150)')
		, [EventType]
        ---Example report parameters: StartDateMacro, EndDateMacro &amp; Currency.
        --, [Start Date] = Convert(XML,[Parameters]).value('(//ParameterValue/Value[../Name="StartDateMacro"])[1]','nvarchar(50)') 
        --, [End Date] = Convert(XML,[Parameters]).value('(//ParameterValue/Value[../Name="EndDateMacro"])[1]','nvarchar(50)') 
        --, [Currency] = Convert(XML,[Parameters]).value('(//ParameterValue/Value[../Name="Currency"])[1]','nvarchar(50)')        
        --, [DeliveryExtension]
        --, [Version]
	    , [LastRunTime]        
		, [LastRunTimeRound] = CASE WHEN [LastRunTime] IS NULL THEN '00:00' ELSE LEFT(CAST(DATEADD(MINUTE, ROUND(DATEDIFF(MINUTE, 0, [LastRunTime]) / 15.0, 0) * 15, 0) AS TIME),5) END
		, [LastStatus]
		, [LastStatusFlag] = CHARINDEX('fail',[LastStatus]) + CHARINDEX('disabled',[LastStatus]) + CHARINDEX('error',[LastStatus]) + CHARINDEX('cancel',[LastStatus])
		, [Failed] = CASE WHEN CHARINDEX('fail',[LastStatus]) > 0 THEN 1 ELSE 0 END
		, [Disabled] = CASE WHEN CHARINDEX('disabled',[LastStatus]) > 0 THEN 'Yes' ELSE 'No' END

    FROM dbo.[Catalog] c
    INNER JOIN dbo.[Subscriptions] S ON c.ItemID = S.Report_OID
    INNER JOIN dbo.ReportSchedule R ON S.SubscriptionID = R.SubscriptionID
    INNER JOIN msdb.dbo.sysjobs J ON Convert(nvarchar(128),R.ScheduleID) = J.name
    INNER JOIN msdb.dbo.sysjobschedules JS ON J.job_id = JS.job_id



GO


