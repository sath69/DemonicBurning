from discord.ext import commands
import discord
import random
import time
from discord import app_commands


class GayCalculator(commands.Cog, name ="Gay Calculator"):
    """Calculates gayness of the user."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    @app_commands.command(
          name="gaycalc",
          description="Calculates gayness of the user."
    )
    async def gaycalc(self, interaction: discord.Interaction, user: discord.Member):
     percent = random.randint(0,100)
     num = random.randint(4,7)
     await interaction.response.send_message("Calculating your gayness...")
     time.sleep(num)
     await interaction.followup.send("Calculated!")
     await interaction.followup.send(f"{user.mention}, you are `{percent}%` gay!")

     
    
async def setup(bot: commands.Bot):
    await bot.add_cog(GayCalculator(bot))