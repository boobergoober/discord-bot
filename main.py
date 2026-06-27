import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os
import sqlite3
import mcpq as mc
import subprocess

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
server_on = False #run the bot first and he should be able to turn the server on

#handling events

@bot.event
async def on_ready():
    print("We are ready to go in, {bot.user.name}")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    await bot.process_commands(message)

@bot.command()
async def tries(ctx):
    await ctx.send(f"You tried the to guess the password {dick[ctx.author.name]} times")

@bot.command()
async def hello(ctx):
    await ctx.send("Hello {} !".format(ctx.author.name))

@bot.command()
async def whitelist(ctx, operat, user, password):
    if server_on == False:
        await ctx.send("server is off")
    elif operat not in ["add", "remove"]:
        await ctx.send("typo")
    elif password == "123":
        try: mc.runCommand(f"whitelist {operat} {user}")
        except: await ctx.send("something went wrong with adding the user...")
    else:
        await ctx.send("wrong password, don't try again")
        if ctx.author.name in dick.keys():
            dick[ctx.author.name] += 1    
        else:
            dick.update({ctx.author.name : 1})

@bot.command()
async def mccommand(ctx, password, command):
    global server_on
    if server_on == False:
        await ctx.send("server is off")
    elif password == 123:
        mc.runCommand(command)
    else:
        await ctx.send("wrong password, don't try again")
        if ctx.author.name in dick.keys():
            dick[ctx.author.name] += 1    
        else:
            dick.update({ctx.author.name : 1})

@bot.command()
async def off(ctx):
    global server_on
    if server_on == False:
        await ctx.send("server is already off!")
    else:
        server_on = False
        await ctx.send("server was turned off")
        subprocess.Popen(["stop"],cwd="/home/etienne/server2406")

@bot.command()
async def on(ctx):
    global server_on
    print(server_on)
    if server_on == True:
        await ctx.send("server is already on!")
    else:
        server_on = True
        await ctx.send("server was turned on")
        try: subprocess.Popen(["bash", "/home/etienne/server2406/start.sh"], cwd="/home/etienne/server2406")
        except: print("something went wrong")

bot.run(token, log_handler = handler, log_level=logging.DEBUG)
