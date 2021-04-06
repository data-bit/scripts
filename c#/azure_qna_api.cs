using System;

using System.Collections.Generic;

using System.Net.Http;

using System.Net.Http.Headers;

using System.Text;

using System.Threading.Tasks;

using Microsoft.Azure.CognitiveServices.Knowledge.QnAMaker;

using Microsoft.Azure.CognitiveServices.Knowledge.QnAMaker.Models;

using Newtonsoft.Json;



namespace CSHttpClientSample

{

    static class Program

    {

        static void Main()

        {

            MakeRequest();

            Console.WriteLine("Hit ENTER to exit...");

            Console.ReadLine();

        }

        

        static async void MakeRequest()

        {

            var question = new { question = "How can I cancel my hotel reservation?"};



            var json = JsonConvert.SerializeObject(question);

            var data = new StringContent(json, Encoding.UTF8, "application/json");



            var url = "https://qnamakermsft.azurewebsites.net/qnamaker/knowledgebases/3fa82422-da5c-4a9a-b8d7-5d0f89d72cbb/generateAnswer";



            using var client = new HttpClient();

            client.DefaultRequestHeaders.Authorization = new AuthenticationHeaderValue("EndpointKey", "9df9246f-2798-47e5-83b0-2d5f8fdda8c4");



            var response = await client.PostAsync(url, data);



            string result = response.Content.ReadAsStringAsync().Result;

            Console.WriteLine(result);

        }

    }

}   