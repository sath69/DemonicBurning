import randfacts
from discord import app_commands
from discord.ext import commands
import discord

class Fact(commands.Cog, name= "fact"):
    """Generates a random fact. Disclaimer: Facts are not guaranteed to be true."""
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    @app_commands.command(
        name="fact",
        description="Generates a random fact. Disclaimer: Facts are not guaranteed to be true."
    )
    async def fact(self, interaction: discord.Interaction):
        fact = randfacts.get_fact()
        await interaction.response.send_message(fact)
    
async def setup(bot: commands.Bot):
    await bot.add_cog(Fact(bot))