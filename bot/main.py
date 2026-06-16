import discord
from dotenv import load_dotenv
import os 
import requests
import json
def fetch_meme(subreddit=None):
    if subreddit is None:
        url = "https://meme-api.com/gimme"
    else:
        url = f"https://meme-api.com/gimme/{subreddit}"
    response = requests.get(url)
    return response.json()
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
@client.event
async def on_ready():
  print(f'Bot is online as {client.user}')
@client.event
async def on_message(message):
  if message.content == '!ping':
   await message.channel.send('pong!')
  elif message.content == '!hello':
   await message.channel.send('Hello! I am MemeBot! 👋')
  elif message.content == '!leaderboard':
   leaderboard = get_leaderboard()
   await message.channel.send(leaderboard)
  elif message.content == '!memeinfo':
    data = fetch_meme()
    await message.channel.send(f'TITLE - {data["title"]}\nSUBREDDIT-{data["subreddit"]}\nUPVOTES-{data["ups"]}\nAUTHOR-{data["author"]}')
 
  elif message.content.startswith('!meme'):
    parts=message.content.split()
    if len(parts)==1:
     data = fetch_meme()
    elif len(parts)==2:
     data = fetch_meme(parts[1])
 
    
    if "code" in data:
     await message.channel.send("❌ That subreddit doesn't exist! Try !meme dankmemes")
    else:
     await message.channel.send(f'{data["title"]}\n{data["url"]}')
     update_score(str(message.author))
def update_score(user):
    with open('scores.json', 'r') as f:
        scores = json.load(f)
    if user in scores:
        scores[user] += 1
    else:
        scores[user] = 1
    with open('scores.json', 'w') as f:
        json.dump(scores, f)

def get_leaderboard():
    with open('scores.json', 'r') as f:
        scores = json.load(f)
    sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    leaderboard = '🏆 Meme Leaderboard 🏆\n'
    for i, (user, score) in enumerate(sorted_scores[:5], 1):
        leaderboard += f'{i}. {user} - {score} memes\n'
    return leaderboard
 
   
client.run(TOKEN)