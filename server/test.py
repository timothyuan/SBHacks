import requests
import json

url = "http://35.235.88.148:3000/check"
file = open('upload.dat', 'rb').read()
r = requests.post(url, file = file)
data = r.json()['isAllowed']
print(data)
