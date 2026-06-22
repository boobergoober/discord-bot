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

#set up the data base :)


def db_start():
    global connection
    connection = sqlite3.connect("curses.db")

cursor = connection.cursor()

cursor.execute("CREATE TABLE IF NOT EXISTS users(username TEXT, shit_count INTEGER)")

def db_retrieveForUser(username):
    cursor.execute("SELECT * FROM users WHERE username='{}'".format(username))
    results = cursor.fetchone()
    return results

def db_isUserInDb(username):
    cursor.execute("")

def db_createNewUser(username, shitcount):
    cursor.execute("INSERT INTO users VALUES('{}', {})".format(username, shitcount))
    connection.commit()

def db_updateUser(username, collumn, value):
    cursor.execute("UPDATE users SET {}={} WHERE username='{}'".format(collumn, value, username))
    connection.commit()
    print("done")

def db_close():
    connection.close()
#prefix

bot = commands.Bot(command_prefix="!", intents= intents)

#handling events

@bot.event
async def on_ready():
    print(f"We are ready to go in, {bot.user.name}")

@bot.event
async def on_message(message):

    await bot.process_commands(message)

    if message.content.startswith("!"):
        return

    scope =""
    local_shit_count = 0
    for i in message.content:
        scope+=i
        if "shit" in scope or "Shit" in scope or "SHIT" in scope:
            scope = ""        
            local_shit_count += 1
            print(local_shit_count)
    try:
        db_start()
        db_shcnt = db_retrieveForUser(message.author)[1]
        db_shcnt = db_shcnt + local_shit_count
        db_updateUser(message.author, "shit_count", db_shcnt)
        db_close()
    except Exception as e:
        print("DB Error:" + e)
    

@bot.command()
async def shitcount(ctx):
    db_start()
    db_shcnt = db_retrieveForUser(ctx.message.author)[1]

    print("here")
    db_close()

    await ctx.send("You said shit {} times !".format(db_shcnt))

@bot.command()
async def hello(ctx):
    await ctx.send("Hello {} !".format(ctx.author.name))
    

bot.run(token, log_handler = handler, log_level=logging.DEBUG)