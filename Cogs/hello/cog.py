from discord.ext import commands
from discord import app_commands
import discord


class Hello(commands.Cog, name ="Hello"):
    """Replies to user with a greeting."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    @app_commands.command(
          name= "hello",
          description="Replies to user with a greeting."
    )
    async def hello(self, interaction: discord.Interaction):
     await interaction.response.send_message(f"Hello, <@{interaction.user.id}>!")
    
async def setup(bot: commands.Bot):
    await bot.add_cog(Hello(bot))