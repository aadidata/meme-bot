import requests
response = requests.get("https://meme-api.com/gimme")
data = response.json()
print(data['title'])
print(data['url'])