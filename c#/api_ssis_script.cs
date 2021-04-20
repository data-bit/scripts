// Author: Mitch Alves (IDP7116)
// Created On: 2020-04-15

using Microsoft.SqlServer.Dts.Runtime;
using System.Net;
using System.IO;
using System.Security.Authentication;

namespace ST_2a4c0d788eba45dd8339d82c44a0cfe7
{

	[Microsoft.SqlServer.Dts.Tasks.ScriptTask.SSISScriptTaskEntryPointAttribute]
	public partial class ScriptMain : Microsoft.SqlServer.Dts.Tasks.ScriptTask.VSTARTScriptObjectModelBase
	{
        
		public void Main()
		{
            // Initialize Security Protocol
            const SslProtocols _Tls12 = (SslProtocols)0x00000C00;
            const SecurityProtocolType tls12 = (SecurityProtocolType)_Tls12;
            ServicePointManager.SecurityProtocol = tls12;

            // Access Variables
            Variables varCollection = null;

            Dts.VariableDispenser.LockForRead("User::RemoteUri");
            Dts.VariableDispenser.LockForRead("User::LocalFolder");
            Dts.VariableDispenser.GetVariables(ref varCollection);

            // Download file via API
            System.Net.WebClient myWebClient = new System.Net.WebClient();
            string webResource = varCollection["User::RemoteUri"].Value.ToString();
            string fileName = varCollection["User::LocalFolder"].Value.ToString() + webResource.Substring(webResource.LastIndexOf('/') + 1);

            // Save File
            byte[] data;
            using (WebClient client = new WebClient())
            {
                data = client.DownloadData(webResource);
            }
            FileInfo file = new System.IO.FileInfo(fileName);
            file.Directory.Create();
            File.WriteAllBytes(file.FullName, data);

            // Read and Store 
            string jsonData = System.IO.File.ReadAllText(fileName);
            Dts.Variables["User::Json"].Value = jsonData;

            Dts.TaskResult = (int)ScriptResults.Success;
        }

      
        enum ScriptResults
        {
            Success = Microsoft.SqlServer.Dts.Runtime.DTSExecResult.Success,
            Failure = Microsoft.SqlServer.Dts.Runtime.DTSExecResult.Failure
        };
      

	}
}