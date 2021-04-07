USE [ReportServer]
GO

SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

-- ===================================================
-- Author:		Mitch Alves (idp7116)
-- Description:	SSRS - Directory Analysis
-- ===================================================

ALTER PROCEDURE [hca].[ssp_SSRS_Directory_Analysis] (@Lv1_Folder VARCHAR(255)) AS
BEGIN
	SET NOCOUNT ON;
	SET TRANSACTION ISOLATION LEVEL READ UNCOMMITTED;	

	/* Debugging */
	DECLARE @Lv1_Folder VARCHAR(255) = 'East Florida Division';
	

	-- LOAD DSS PARAMETERS
	IF OBJECT_ID('tempdb.dbo.#ParamList', 'U') IS NOT NULL DROP TABLE #ParamList;
	CREATE TABLE #ParamList (ReportPath VARCHAR(255), ParameterName VARCHAR(255), DataSetName VARCHAR(255));
	INSERT INTO #ParamList EXEC hca.ssp_SSRS_List_Parameters_DSS;
	-- GROUP and CONCATENATE
	IF OBJECT_ID('tempdb.dbo.#ReportParameters', 'U') IS NOT NULL DROP TABLE #ReportParameters;
	CREATE TABLE #ReportParameters (ReportPath VARCHAR(255), [Parameters] VARCHAR(999));
	INSERT INTO #ReportParameters (ReportPath, [Parameters])
	SELECT p1.ReportPath
	     , (SELECT ParameterName + ', ' FROM #ParamList p2 WHERE p2.ReportPath = p1.ReportPath ORDER BY ParameterName FOR XML PATH(''))
    FROM #ParamList p1 GROUP BY ReportPath;


	-- LOAD DSS SUBSCRIPTIONS
	IF OBJECT_ID('tempdb.dbo.#SubsList', 'U') IS NOT NULL DROP TABLE #SubsList;
	CREATE TABLE #SubsList (ReportPath VARCHAR(255), Subscriptions VARCHAR(MAX));
	INSERT INTO #SubsList (ReportPath, Subscriptions)	
	SELECT c.path
		 , STUFF(
				 ( SELECT DISTINCT ' [Name] ' + s.[description] + '--- [Last Exec] ' + CAST(s.LastRunTime AS VARCHAR) + '--- [Status] '+ s.LastStatus +'---'
				   FROM dbo.Subscriptions s2 INNER JOIN dbo.[Catalog] AS c2 ON c2.ItemID = s2.Report_OID
				   WHERE c2.[Path] = c.[Path]
				   FOR XML PATH ('')
				 ), 1, 1, ''
			)  AS Subscriptions
	FROM dbo.Subscriptions s 
	INNER JOIN dbo.[Catalog] c 
		ON s.Report_OID = c.ItemID 
	WHERE s.EventType = 'TimedSubscription' AND c.[Path] LIKE '%DSS%'	
	GROUP BY c.Path, s.Description, s.LastStatus, s.LastRunTime;
	-- GROUP and CONCATENATE
	IF OBJECT_ID('tempdb.dbo.#ReportSubscriptions', 'U') IS NOT NULL DROP TABLE #ReportSubscriptions;
	CREATE TABLE #ReportSubscriptions (ReportPath VARCHAR(255), Subscriptions VARCHAR(MAX));
	INSERT INTO #ReportSubscriptions (ReportPath, Subscriptions)
	SELECT s.ReportPath
		 , STUFF(
				 ( SELECT DISTINCT ' @@@ ' + s2.Subscriptions
				   FROM #SubsList s2 WHERE s2.ReportPath = s.ReportPath
				   FOR XML PATH ('')
				 ), 1, 1, ''
			)  AS Subscriptions
	FROM #SubsList s GROUP BY s.ReportPath;

	-- OUTPUT
	WITH Directory AS
	(
		SELECT DISTINCT 
			  'Division_Name' = ( SELECT item FROM dbo.tvf_SplitCustomStrings (c.[Path], '/') WHERE id = 2 ) 
			, 'Dir_Lv1'		  = ( SELECT item FROM dbo.tvf_SplitCustomStrings (c.[Path], '/') WHERE id = 3 ) 
			, 'Dir_Lv2'		  = ( SELECT item FROM dbo.tvf_SplitCustomStrings (c.[Path], '/') WHERE id = 4 ) 
			, 'Dir_Lv3'		  = ( SELECT item FROM dbo.tvf_SplitCustomStrings (c.[Path], '/') WHERE id = 5 ) 
			, 'Link'		  = REPLACE('http://efdvwpapprpt02.hca.corpad.net/Reports/report'+ C.[Path], ' ', '%20')
			, 'Description'	  = c.Description 
			, 'ReportPath'	  = c.Path 
		FROM dbo.[Catalog] c WITH (NOLOCK)
		WHERE c.[Type] = 2 AND c.[Hidden] = 0
	)
	SELECT DISTINCT d.Division_Name, d.Dir_Lv1, d.Dir_Lv2, d.Dir_Lv3, d.Description, d.Link
				  , REPLACE(REPLACE(p.Parameters, 'Division_Id, ',''),'Division, ','') AS Parameters				  
				  --, '/Images/' + d.Dir_Lv2 +'/'+ d.Dir_Lv3 + '.png' AS Image_Link
				  , CASE WHEN s.Subscriptions IS NULL THEN '' ELSE  s.Subscriptions END Subscriptions
	FROM Directory d
	LEFT JOIN #ReportParameters p ON p.ReportPath = d.ReportPath COLLATE Latin1_General_100_CI_AS_KS_WS	
	LEFT JOIN #ReportSubscriptions s ON s.ReportPath = d.ReportPath COLLATE Latin1_General_100_CI_AS_KS_WS
	WHERE d.Division_Name IN (SELECT Item FROM [dbo].[tvf_SplitString] (@Lv1_Folder,',')) 
	  AND d.Dir_Lv1 NOT IN ('some folder') 
	  AND d.Dir_Lv2 NOT IN ('some other folder') ;
	
END
