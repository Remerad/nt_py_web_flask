import requests
# response = requests.post(
#     'http://127.0.0.1:5500/advertisement',
#     headers={'header_1': '1'},
#     json={
#         'heading': 'Продам мопед4',
#         'description': 'Мопед не мой, я просто разместил объяву',
#         'owner': 'Вася'
#     }
# )
# response = requests.get(
#     'http://127.0.0.1:5500/advertisement',
#     headers={'header_1': '1'},
#     json={
#         'heading': 'Продам мопед1',
#         'description': 'Мопед не мой, я просто разместил объяву',
#         'owner': 'Вася'
#     }
# )
response = requests.delete(
    'http://127.0.0.1:5500/advertisement',
    json={
        'heading': 'Продам мопед1'
    }
)
print(response.status_code)
print(response.headers)
print(response.text)