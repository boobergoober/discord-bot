import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os
import sqlite3

load_dotenv()

token = os.getenv("DISCORD_TOKEN")
 
handler = logging.FileHandler(filename="discord.log", encoding="utf-8", mode="w")
intents = discord.Intents.default()
intents.message_content = True
intents.members = True


#prefix

bot = commands.Bot(command_prefix="!", intents= intents)

# Shit-count, restoring the dictionary
    
dick = {}

#handling events

@bot.event
async def on_ready():
    print("We are ready to go in, {bot.user.name}")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if "shit" in message.content and message.content != "!shit_count":
        print("doing something?")
        if message.author.name in dick.keys():
            dick[message.author.name] += 1    
        else:
            dick.update({message.author.name : 1})    
        print("didnt get stuck")

    print(dick)

    await bot.process_commands(message)

@bot.command()
async def shit_count(ctx):
    await ctx.send("You said shit {} times !".format(dick[ctx.author.name]))

bot.run(token, log_handler = handler, log_level=logging.DEBUG)