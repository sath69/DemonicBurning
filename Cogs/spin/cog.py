from discord.ext import commands
from main import *
import time
import discord
import random
import discord
from discord import app_commands


class Spin(commands.Cog, name ="Spin"):
    """Spins the Fruit Machine™."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    @app_commands.command(
          name="spin",
          description="Spins the Fruit Machine™."

    )
    @app_commands.checks.cooldown(1,2)
    async def spin(self, interaction: discord.Interaction):
     member = interaction.user
  
     
     
     cursor = db.cursor()

     cursor.execute(f"""SELECT wallet FROM economy WHERE user_id = ('%s')""" % (member.id) )
     wallet = cursor.fetchone()
     try:
        wallet = wallet[0]
     except:
        wallet = 0

     cherry = "🍒"
     bell = "🔔"
     lemon = "🍋"
     orange = "🍊"
     star = "⭐"
     skull = "💀"
     credit = wallet

     embed = discord.Embed(colour=discord.Colour.dark_gold(),title = "**Fruit Machine™**")

     if wallet < 0.20:
         await interaction.response.send_message(f"You haven't got enough money to play the Fruit Machine!\nYour balance currently is £{wallet:0.2f}.")
         return
   
     while credit > 0:
      fruitList = [cherry,bell,lemon,orange,star,skull]
      spinner = []
      skullcounter = 0
      skullcounter = 0
      if credit == 0:
        await interaction.response.send_message("You have no more money.")
      for i in range(0,3):
       adder = random.choice(fruitList)
       spinner.append(adder)
      await interaction.response.send_message("ROLLING...")
      time.sleep(0.5)
      credit -= 0.20
      embed.add_field(name = "**Result:**", value = f"{spinner[0]}{spinner[1]}{spinner[2]}", inline= False)
      if spinner[0] == skull:
         skullcounter += 1
      if spinner[1] == skull:
         skullcounter += 1
      if spinner[2] == skull:
         skullcounter += 1
      if skullcounter == 2:
        embed.add_field(name= "**Lost Money:**",value="You lost £1", inline= False)
        credit -= 1.00
        spinner.clear()
        break
      if skullcounter == 3:
         await interaction.response.send_message("You lost all your money.Game Over.")
         credit -= credit
         break
      if spinner[0] == spinner[1] or spinner[1] == spinner[2] or spinner[0] == spinner[2]:
        if spinner[0] == spinner[1] and spinner[1] == spinner[2] and spinner[0] == spinner[2]:
          if spinner[0::] == bell:
            credit += 5.00
            embed.add_field(name= "**Won Money:**",value="You won £5. Excellent!",  inline= False)
            spinner.clear()
            break
          embed.add_field(name= "**Won Money:**",value="You won £1. Well done!",  inline= False)
          credit += 1.00
          spinner.clear()
          break
        embed.add_field(name= "**Won Money:**",value="You won 50p. Not bad!",  inline= False)
        credit += 0.50
        spinner.clear()
      spinner.clear()
      if credit < 0:
        await interaction.response.send_message("You have no more money.")
        break
      break

     sql = ("""UPDATE economy SET wallet = %s WHERE user_id = %s """)
     val = (float(credit), member.id)
     cursor.execute(sql,val)
     embed.add_field(name= "**Balance:**", value = f"Your balance currently is **£**`{credit:0.2f}`.",  inline= False)
     embed.set_footer(text="Sponsored by Demonic Economy")
     await interaction.followup.send(embed=embed)

     db.commit()
     cursor.close()


     
    
async def setup(bot: commands.Bot):
    await bot.add_cog(Spin(bot))