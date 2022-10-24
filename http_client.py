import requests
response = requests.post(
    'http://127.0.0.1:5500/advertisement',
    headers={'header_1': '1'},
    json={
        'heading': 'Продам мопед2',
        'description': 'Мопед не мой, я просто разместил объяву',
        'owner': 'Вася'
    }
)
print(response.status_code)
print(response.headers)
print(response.text)