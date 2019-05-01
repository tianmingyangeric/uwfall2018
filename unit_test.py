import http.client
import os


url = "http://localhost:8080/?user=1"
conn = http.client.HTTPConnection('localhost:8080')
conn.request(method="GET", url=url)
response = conn.getresponse()
res = str(response.read())
print(res)

result = res.split(';')
print(result)