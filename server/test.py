import requests
import json

url = "http://localhost:3000/check"
files = {'file': open('upload.dat', 'rb')}
r = requests.post(url, files=files)
data = r.json()['isAllowed']
print(data)
