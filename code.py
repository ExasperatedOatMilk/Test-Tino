import discord
import os
import requests
import json
import asyncio
from better_profanity import profanity
from replit import db
import time
from discord.ext import commands

no_swearing = True

db["user_data"] = {}
user_messages = {}
messages = joined = 0

bot = commands.Bot(command_prefix='!T ')

client = discord.Client()


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

      await asyncio.sleep(60**2)

    except Exception as e:
      print(e)
      await asyncio.sleep(60**2)


async def member_join(member):
  global joined
  for channel in member.server.channels:
    if channel == "ok-boomer":
      await client.send_message(f"Welcome to the server |{member.mention}|")
      joined += 1


async def kick(ctx,member: discord.Member,*, reason=None):
  await member.kick(reason=reason)
  await ctx.send(f'User {member} has kicked.')

@bot.command()
async def say(ctx, message=None):
  await ctx.send(message)

async def quote(ctx):
  response = requests.get('https://zenquotes.io/api/random')

  json_data = json.loads(response.text)
  quote = json_data[0]["q"] + "~ " +json_data[0]["a"]
  await ctx.send(quote)

async def help(ctx):
  file = open("Help.txt")
  await ctx.send(file.read())

async def delete(ctx, message=None):
  if (message.split())[2] == "all":
    await message.channel.purge(limit=1234567890123456789012345678990123456789012345678901234567898675423456787654323456)

  else:
    await message.channel.purge(limit=(int((((message).lower()).split())[2])))

  await ctx.send(message)

async def no_swearing(ctx,message=None):
  global no_swearing
  if ((message.split())[2]).lower() == "off":no_swearing = False
  else: no_swearing = True



@client.event
async def on_ready():
  print("I Am Online")
  await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="!T help"))
  await client.get_channel.send("Swearing is automatically on, to disable it, type '!T no_swearing off' and '!T no_swearing on' enable it")

async def on_message(message):
  global messages,user_messages
  msg = message.content
  if message.author == client.user:return

  if message.author not in user_messages: user_messages[message.author] = 0
  user_messages[message.author] += 1

  if profanity.contains_profanity(message.content) and no_swearing:
    await message.channel.purge(limit=1)
    await message.channel.send(f"{message.author}: sent something not so cool".format(client))

  messages += 1
  if "!T ignore" not in message.content: print((message.author),"sent: ".format(client),msg)



client.loop.create_task(update_stats())

client.run(os.environ['TOKEN'])
