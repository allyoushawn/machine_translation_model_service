import requests

url = "http://127.0.0.1:4460/sentiment_analysis"
data = {"text": "This is very good."}
x = requests.post(url, json=data)
print(x.json()["response"])