import requests

url = 'http://localhost:5000/predict_api'
r = requests.post(url,json={'loc':2, 'time':9})

print(r.json())