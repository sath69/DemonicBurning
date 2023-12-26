from discord.ext import commands
import requests
import discord
from discord import app_commands


class Quote(commands.Cog, name ="Quote"):
    """Replies to user with a random quote."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    @app_commands.command(
            name="quote",
            description="Replies to user with a random quote."
    )
    async def quote(self, interaction: discord.Interaction):
      api =  "http://api.quotable.io/random"
      random_quote = requests.get(api).json()
      content = random_quote["content"]
      author = random_quote["author"]
      quote = f"**{content}**\nBy:`{author}`"
      await interaction.response.send_message(quote)

    
     
    
async def setup(bot: commands.Bot):
    await bot.add_cog(Quote(bot))