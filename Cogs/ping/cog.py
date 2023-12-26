from discord.ext import commands
from discord import app_commands
import discord



class Ping(commands.Cog, name ="Ping"):
    """Responds with 'Pong' with latency."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    @app_commands.command(
            name= "ping",
            description="Responds 'Pong' with latency."
    )
    async def ping(self, interaction: discord.Interaction):
      await interaction.response.send_message(f':ping_pong: Pong!\n**Latency:** `{round(self.bot.latency * 1000)}`*ms*')
    
async def setup(bot: commands.Bot):
    await bot.add_cog(Ping(bot))