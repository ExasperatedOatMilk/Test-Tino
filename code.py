import discord
import os
import requests
import json
import asyncio
from replit import db
import time
user_messages = {}
messages = joined = 0

client = discord.Client()

def get_quote():
  response = requests.get('https://zenquotes.io/api/random')

  json_data = json.loads(response.text)
  quote = json_data[0]["q"] + "~ " +json_data[0]["a"]
  return quote

async def update_stats():
  global messages, joined
  await client.wait_until_ready()
  while not client.is_closed():
    try:
      with open("stats.txt","a") as f:
        f.write(f"Time: {int(time.time())}, Messages: {messages}, Members Joined: {joined}\n")

      messages = 0
      joined = 0

      with open("user_messages.txt","a") as f:
        f.write(f"{user_messages}\n\n\n")

      await asyncio.sleep(5)

    except Exception as e:
      print(e)
      await asyncio.sleep(5)


async def member_join(member):
  global joined
  for channel in member.server.channels:
    if channel == "ok-boomer":
      await client.send_message(f"Welcome to the server |{member.mention}|")
      joined += 1



@client.event
async def on_ready():
  print("I Am Online")
  await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="!T help"))

db["user_data"] = {}

@client.event
async def on_message(message):
  global messages,user_messages
  msg = message.content
  if message.author == client.user:return

  elif msg.startswith('!T '):

    if msg.startswith('!T ignore'):return

    elif (((msg).lower()).split())[1] == "help":
      file = open("Help.txt")
      await message.channel.send(file.read())

    elif (((msg).lower()).split())[1] == "code":
      print("send link")

    elif (((msg).lower()).split())[1] == "quote":
      await message.channel.send(get_quote())
    
    elif (((msg).lower()).split())[1] == "del" and (((msg).lower()).split())[2] != "all":await message.channel.purge(limit=(int((((msg).lower()).split())[2])))

    elif (((msg).lower()).split())[1] == "del":await message.channel.purge(limit=1234567890123456789012345678990123456789012345678901234567898675423456787654323456)

  if message.author not in user_messages: user_messages[message.author] = 0
  user_messages[message.author] += 1

  messages += 1
  print(message.author,"sent: ".format(client),msg)



client.loop.create_task(update_stats())

client.run(os.environ['TOKEN'])

