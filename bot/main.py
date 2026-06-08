import discord
from dotenv import load_dotenv
import os 
import requests
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
 
   
client.run(TOKEN)