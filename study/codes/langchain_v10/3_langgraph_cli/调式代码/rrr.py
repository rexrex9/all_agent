import requests

url = 'http://127.0.0.1:8080/hello2'
res = requests.get(url)
print(res.text)