import requests

email = 'manishkanth@gmail.com'
api_key = 'e1cf42b7-9c9a-4dd0-8748-a5cb7c147665'
url = f'https://api.mails.so/v1/validate?email={email}'

headers = {
    'x-mails-api-key': api_key
}

response = requests.get(url, headers=headers)
data = response.json()
print(data)
  