import requests
from requests.structures import CaseInsensitiveDict

url = "https://qnamakermsft.azurewebsites.net//qnamaker/knowledgebases/3fa82422-da5c-4a9a-b8d7-5d0f89d72cbb/generateAnswer"

headers = CaseInsensitiveDict()
headers["Accept"] = "application/json"
headers["Authorization"] = "EndpointKey 9df9246f-2798-47e5-83b0-2d5f8fdda8c4"
headers["Content-Type"] = "application/json"

data = '{"question":"How do i book a flight"}'

resp = requests.post(url, headers=headers, data=data)

print(resp.content)