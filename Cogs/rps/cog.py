from discord import app_commands
from discord.ext import commands
import discord
import random
from main import *


class RPS(commands.Cog, name="RPS"):
    """Rock Paper Scissors. Player VS AI"""
    
    def __init__(self, bot: commands.Bot):
       self.bot = bot
    
    @app_commands.command(
        name="rps",
        description="Rock Paper Scissors. Player VS AI"
    )
    @app_commands.checks.cooldown(1,2)
    @app_commands.describe(rps ="Choose either rock, paper or scissors.")
    @app_commands.choices(rps =
                          [discord.app_commands.Choice(name = "Rock", value=1),
                          discord.app_commands.Choice(name = "Paper", value=2),
                          discord.app_commands.Choice(name = "Scissors", value=3),]
                        )
    async def rps(self, interaction: discord.Interaction, rps: discord.app_commands.Choice[int]):
        member = interaction.user
        cursor = db.cursor()
        cursor.execute(f"""SELECT wallet FROM economy WHERE user_id = ('%s')""" % (member.id) )
        wallet = cursor.fetchone()
        try:
           wallet = wallet[0]
        except:
           wallet = 0
        
        options = ["Rock", "Paper", "Scissors"]
        player = rps
        isWon = False
        computer = random.choice(options)
        e = discord.Embed(colour=discord.Colour.dark_blue(), title="**Rock, Paper, Scissors:**")
        if rps.name == computer:
            e.add_field(name="**Result:**",value="`You both tie!`", inline= False)
        elif rps.name == "Rock" and computer == "Scissors":
            e.add_field(name="**Result:**",value="`You win!`", inline= False)
            isWon = True
        elif rps.name == "Scissors"and computer == "Paper":
            e.add_field(name="**Result:**",value="`You win!`", inline= False)
            isWon = True
        elif rps.name == "Paper" and computer == "Rock":
            e.add_field(name="**Result:**",value="`You win!`", inline= False)
            isWon = True
        #if it is not in the list
        elif rps.name not in options:
            await interaction.response.send_message("**ERROR:** You must type either rock, paper or scissors.")
            return
        else:
            compensation = 0.15
            e.add_field(name="**Result:**",value="`You lost!`", inline= False)
            sql = ("""UPDATE economy SET wallet = %s WHERE user_id = %s """)
            val = (wallet - float(compensation), member.id)
            cursor.execute(sql,val)
            e.add_field(name="**Compensation:**",value=f"You lost `15`p...", inline= False)
            bal = wallet - float(compensation)
            e.add_field(name="**Balance:**", value=f"You have **£**`{bal:0.2f}` left in your wallet.")
            db.commit()
            cursor.close()
        if isWon == True:
            reward = 0.10
            sql = ("""UPDATE economy SET wallet = %s WHERE user_id = %s """)
            val = (wallet + float(reward), member.id)
            cursor.execute(sql,val)
            e.add_field(name="**Reward:**",value=f"You have got `10`p!", inline= False)
            bal = wallet + float(reward)
            e.add_field(name="**Balance:**", value=f"You have **£**`{bal:0.2f}` left in your wallet.")
            db.commit()
            cursor.close()

        if rps.name == "Rock":
            player = ":rock: - Rock"
        if rps.name == "Paper":
           player = ":newspaper: - Paper"
        if rps.name == "Scissors":
            player = ":scissors: - Scissors"
        if computer == options[0]:
            computer = ":rock: - Rock"
        if computer == options[1]:
            computer = ":newspaper: - Paper"
        if computer == options[2]:
            computer = ":scissors: - Scissors"
        e.add_field(name="**Player:**",
                    value= f"{player}", inline=False)
        e.add_field(name="**AI:**",
                    value= f"{computer}", inline=False)
        e.set_footer(text="Sponsored by Demonic Economy")
        e.set_thumbnail(url="https://images.squarespace-cdn.com/content/v1/618037d25050485b61e7f62d/271f0feb-c872-4eb6-b918-3e9c8e38443c/Rock+Paper+Scissors+Logo.png")
        await interaction.response.send_message(embed=e)

async def setup(bot: commands.Bot):
   await bot.add_cog(RPS(bot))
          

        