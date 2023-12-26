from discord.ext import commands
from discord import app_commands
import discord


class fm(commands.Cog, name ="Fruit Machine Rules"):
    """List of the Fruit Machine rules and guidance."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    @app_commands.command(
            name="fmrules",
            description="List of the Fruit Machine rules and guidance."
    )
    async def fm(self, interaction: discord.Interaction):
      await interaction.response.send_message("`1`The player(YOU) starts with **£1**.\n`2`**20p** would be taken away for each spin.\n`3`If the Fruit Machine™ rolls **two** of the same symbol the user wins **50p**.\n`4`The player wins £1 for three of the same and £5 for **3** Bells.\n`5`The player loses **£1** if **two** skulls are rolled and **all** of his/her money if **three** skulls are rolled.")

    
    
async def setup(bot: commands.Bot):
    await bot.add_cog(fm(bot))