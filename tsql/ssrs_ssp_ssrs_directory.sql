USE [ReportServer]
GO

SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
-- ===================================================
-- Author:		Nitch Alves
-- Description:	SSRS - Directories and Files
-- ===================================================

ALTER PROCEDURE [hca].[ssp_SSRS_Directory] (@Division_Name VARCHAR(255), @Dir_Lv1 VARCHAR(999), @Dir_Lv2 VARCHAR(999)/*, @Dir_Lv3 VARCHAR(999)*/) AS
BEGIN
	SET NOCOUNT ON;
	SET TRANSACTION ISOLATION LEVEL READ UNCOMMITTED;	
	/*DECLARE @Division_Name VARCHAR(255) = 'East Florida Division';
	DECLARE @Dir_Lv1 VARCHAR(255) = 'DSS';
	DECLARE @Dir_Lv2 VARCHAR(255) = 'Details';  
	DECLARE @Dir_Lv3 VARCHAR(255) = 'EFL - Observation Cases Details';  */

	WITH Directory AS
	(
		SELECT DISTINCT 
			    'Division_Name' = ( SELECT item FROM dbo.tvf_SplitCustomStrings (c.Path, '/') WHERE id = 2 ) ,
				'Dir_Lv1'	= ( SELECT item FROM dbo.tvf_SplitCustomStrings (c.Path, '/') WHERE id = 3 ) ,
				'Dir_Lv2'	= ( SELECT item FROM dbo.tvf_SplitCustomStrings (c.Path, '/') WHERE id = 4 ) ,
				'Dir_Lv3'	= ( SELECT item FROM dbo.tvf_SplitCustomStrings (c.Path, '/') WHERE id = 5 ) ,
				'Dir_Lv4'	= ( SELECT item FROM dbo.tvf_SplitCustomStrings (c.Path, '/') WHERE id = 6 )
		FROM dbo.Catalog c WITH (NOLOCK)
		WHERE c.Type = 2
	)
	SELECT DISTINCT Division_Name, Dir_Lv1, Dir_Lv2, Dir_Lv3, Dir_Lv4
	FROM Directory
	WHERE Division_Name IN (SELECT Item FROM [dbo].[tvf_SplitString] (@Division_Name,',')) 
	  AND Dir_Lv1 IN (SELECT Item FROM [dbo].[tvf_SplitString] (@Dir_Lv1,',')) 
	  AND Dir_Lv2 IN (SELECT Item FROM [dbo].[tvf_SplitString] (@Dir_Lv2,',')) 
	  --AND Dir_Lv3 IN (SELECT Item FROM [dbo].[tvf_SplitString] (@Dir_Lv3,',')) 

END


