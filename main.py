#discord modules
import discord
from discord.ext import commands
from colorama import Fore, Back, Style
from discord import app_commands

#database modules
import psycopg2 as postgresdb

#CoC API modules
import coc
import logging

#asyncio module
import asyncio

#system modules
import os

f = open("token.txt", "r")
token = f.read()
intents = discord.Intents.default()
intents.message_content = True
cogs = os.listdir("Cogs")
bot = commands.Bot(command_prefix = "!", intents=intents, status = discord.Status.online, activity=discord.Game(name=f"Total Commands: {len(cogs)}"))

#connect to database. ONLY WORKS IN HOSTING DATABASE, REMOTE REQUIRES SSH CONNECTION.
connectionData = {
            'database': 'DATABASE_NAME',
             'user': 'DATABASE_USER',
             'password': 'DATABASE PASSWORD',
             'host': 'localhost',
             
         }     
db = postgresdb.connect(**connectionData)

#events
@bot.event
async def on_ready():
    
    #Loads user's online status
    print(f'{Fore.LIGHTCYAN_EX}{Back.BLACK}{bot.user} is online{Fore.RESET}{Back.RESET}')
    
    #loads commands via Cogs
    for folder in os.listdir("Cogs"):
     if os.path.exists(os.path.join("Cogs", folder, "cog.py")):
        await bot.load_extension(f"Cogs.{folder}.cog")

    try:
        synced = await bot.tree.sync()
        print(f"{Fore.YELLOW}Synced {len(synced)} commands.{Fore.RESET}")
    except Exception as e:
        print(e)

@bot.tree.error
async def cog_command_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
    if isinstance(error, app_commands.CommandOnCooldown):
      await interaction.response.send_message(f"Ayo! {interaction.user.mention}, slow down... Try again after {error.retry_after:0.2f} seconds!")
    else:
      raise error   


#Detects if user has sent a message. Automatically creates an object in database.
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    author = message.author
    cursor = db.cursor()
    cursor.execute(f"""SELECT user_id FROM economy WHERE user_id = ('%s')""" % (author.id) )
    result = cursor.fetchone()
    if result is None:
        sql = ("INSERT INTO economy(user_id, wallet, bank) VALUES (%s, %s ,%s)")
        val = (author.id, 1.00,0)
        cursor.execute(sql, val)

    db.commit()
    cursor.close()

    await bot.process_commands(message)

#Connections
async def main():
    logging.basicConfig(level=logging.ERROR)

    async with coc.Client() as coc_client:
        # Attempt to log into CoC API using your credentials.
        try:
            await coc_client.login("DEVPASSWORD","DEVEMAIL")
            print(f"{Fore.GREEN}Successfully connected to CoC API!")
        except coc.InvalidCredentials as error:
            exit(f"{error}")
        # Add the bot session to the bot
        bot.coc_client = coc_client
        await bot.start(str(token))
        
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass

