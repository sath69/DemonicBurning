from discord.ext import commands
import random
import discord
from discord import app_commands
from main import *



class Earn(commands.Cog, name ="earn"):
  """Work to earn money. Only gets added to your wallet."""

  def __init__(self, bot: commands.Bot):
      self.bot = bot
    
  @app_commands.command(
          name = "earn",
          description="Work to earn money. Only gets added to your wallet."
  )
  @app_commands.checks.cooldown(1,20)
  async def earn(self, interaction: discord.Interaction):
   member = interaction.user

   earnings = random.randint(10,40)
   earnings_float = earnings / 100
   
   cursor = db.cursor()
   cursor.execute(f"""SELECT wallet FROM economy WHERE user_id = ('%s')""" % (member.id) )
   wallet = cursor.fetchone()
   try:
        wallet = wallet[0]
   except:
        wallet = 0

   sql = ("""UPDATE economy SET wallet = %s WHERE user_id = %s """)
   val = (wallet + float(earnings_float), member.id)
   cursor.execute(sql,val)
   bal = wallet + float(earnings_float)
   embed = discord.Embed(colour=discord.Colour.dark_purple(),title = "**Demonic Industries**")
   embed.add_field(name= "**Earnings:**",value=f"You have earnt £{earnings_float:0.2f}.", inline=False)
   embed.set_footer(text="Sponsored by Demonic Economy")
   db.commit()
   cursor.close()
   embed.add_field(name="**Balance:**",value=f"Your balance currently is £{bal:0.2f}")
   await interaction.response.send_message(embed=embed)

    
async def setup(bot: commands.Bot):
    await bot.add_cog(Earn(bot))