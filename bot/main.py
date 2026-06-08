import discord
from dotenv import load_dotenv
import os 
import requests
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
    response = requests.get("https://meme-api.com/gimme")
    data = response.json()
    await message.channel.send(f'TITLE - {data["title"]}\nSUBREDDIT-{data["subreddit"]}\nUPVOTES-{data["ups"]}\nAUTHOR-{data["author"]}')
  elif message.content.startswith('!meme'):
    parts=message.content.split()
    if len(parts)==1:
     url=f"https://meme-api.com/gimme"
    elif len(parts)==2:
     url=f"https://meme-api.com/gimme/{parts[1]}"
    response = requests.get(url)
    data = response.json()
    if "code" in data:
     await message.channel.send("❌ That subreddit doesn't exist! Try !meme dankmemes")
    else:
     await message.channel.send(f'{data["title"]}\n{data["url"]}')
 
   
client.run(TOKEN)