import requests


URL = 'http://127.0.0.1:5000/currency/trade/EUR/USD'
data = {'data': {'amount': 50, 'id_user': 1}}
req = requests.post(URL, json=data)

print(req.status_code)