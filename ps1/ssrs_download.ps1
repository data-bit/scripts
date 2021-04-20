#------------------------------------------------------
#Prerequisites
#Install-Module -Name ReportingServicesTools
#------------------------------------------------------

#Lets get security on all folders in a single instance
#------------------------------------------------------
#Declare SSRS URI
$sourceRsUri = 'http://efdvwpapprpt02.hca.corpad.net/ReportServer/'

#Declare Proxy so we dont need to connect with every command
$proxy = New-RsWebServiceProxy -ReportServerUri $sourceRsUri

#Output ALL Catalog items to file system
Out-RsFolderContent -Proxy $proxy -RsFolder / -Destination '\\tpdcipdiv01-efdv.hca.corpad.net\EFDV\Dept\EDFL\SIG\SSRS_Backup' -Recurse