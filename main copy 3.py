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
    connection = sqlite3.connect("latestcurses.db")
    global cursor   #VERY important, previous mistake was that cursor was declared OUTSIDE of start() and since, after being turned off originally cursor is undefined, so everything broke down 
    cursor = connection.cursor()
    
db_start()

cursor.execute("CREATE TABLE IF NOT EXISTS users(username TEXT, shit_count INTEGER)")

def db_retrieveForUser(username):
    cursor.execute("SELECT * FROM users WHERE username='{}'".format(username))
    results = cursor.fetchone()
    return results

def db_isUserInDb(username):
    print("username: " +str(username))
    print("checking...")
    cursor.execute("SELECT username FROM users ")
    results = cursor.fetchone()
    print(results)
    if username in results:
        return True
    else:
        return False

def db_createNewUser(username, shitcount):
    cursor.execute("INSERT INTO users VALUES('{}', {})".format(username, shitcount))

def db_updateUser(username, collumn, value):
    cursor.execute("UPDATE users SET {}={} WHERE username='{}'".format(collumn, value, username))
    print("done")

def db_close():
    connection.commit()
    connection.close()

db_close()

#prefix

bot = commands.Bot(command_prefix="!", intents= intents)

#functions for the bot:

def shit_count_in_message(message):
    scope =""
    local_shit_count = 0
    for i in message.content:
        scope+=i
        if "shit" in scope or "Shit" in scope or "SHIT" in scope:
            scope = ""        
            local_shit_count += 1

    print(local_shit_count)

    db_start() #opens the database to check if user is in there

    if db_isUserInDb(message.author) == False:
        print("he is not in Db")
        db_createNewUser(message.author, 0) #adds the new guy to the data base

    db_close()

    try:    #try to count his shits
        db_start()
        db_shcnt = db_retrieveForUser(message.author)[1]
        db_shcnt = db_shcnt + local_shit_count
        db_updateUser(message.author, "shit_count", db_shcnt)
        db_close()
    except Exception as e:
        print("DB Error:" + e)
    print("finished gud")

#handling events

@bot.event
async def on_ready():
    print(f"We are ready to go in, {bot.user.name}")

@bot.event
async def on_message(message):

    await bot.process_commands(message)

    if message.content.startswith("!"):
        return
    
    if message.author == bot.user.name:
        print("request diguarded")
        return

    shit_count_in_message(message)

@bot.command()
async def shitcount(ctx):
    #open the Db and retrieve the amount of shits!
    db_start()
    db_shcnt = db_retrieveForUser(ctx.message.author)[1]
    db_close()

    await ctx.send("You said shit {} times !".format(db_shcnt))

@bot.command()
async def hello(ctx):
    #just a test function
    await ctx.send("Hello {} !".format(ctx.author.name))

@bot.command()
async def update_my_shit_count(channel):
    messages = [message async for message in channel.history(limit=123)]
    for i in messages:
        shit_count_in_message(i)  
        

    

#connect? its the token for the bot or smth    
bot.run(token, log_handler = handler, log_level=logging.DEBUG)