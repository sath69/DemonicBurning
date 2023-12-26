from discord.ext import commands
import discord
from main import *
from discord import app_commands



class Balance(commands.Cog, name ="balance"):
    """Checks user's balance for wallet and bank."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    @app_commands.command(
          name = "balance",
          description="Checks user's balance for wallet and bank."
    )
    async def balance(self, interaction: discord.Interaction, member: discord.Member = None):
     if member == None:
        member = interaction.user
    
     cursor = db.cursor()

     cursor.execute(f"""SELECT wallet, bank FROM economy WHERE user_id = ('%s')""" % (member.id) )
     bal = cursor.fetchone()
     try:
        wallet = bal[0]
        bank = bal[1]
     except:
        wallet = 0
        bank = 0
     embed = discord.Embed(colour=discord.Colour.dark_teal(),title = "**Demonic Economy**")
     embed.add_field(name="**Wallet:**\n",value=f"**£**`{wallet:0.2f}`")
     embed.add_field(name = "**Bank:**\n",value =f"**£**`{bank:0.2f}`")
     embed.add_field(name="**User:**\n", value = f"*{member}*", inline=False)
     embed.set_thumbnail(url=member.avatar)
     embed.set_footer(text="Powered by Demonic Economy")
                          
     await interaction.response.send_message(embed=embed)
     db.commit()
     cursor.close()
    
    
async def setup(bot: commands.Bot):
    await bot.add_cog(Balance(bot))