import requests
import json

url = "http://100.111.62.92:8000/api/generate"
data = {
    "model": "mistral:7b",
    "prompt": "Write a short poem about coding.",
    "stream": True
}

with requests.post(url, json=data, stream=True) as response:
    print("Status code:", response.status_code)
    for line in response.iter_lines():
        if line:
            shit = json.loads(line.decode("utf-8"))
            print(shit.get("response",""), end="",flush=True)
