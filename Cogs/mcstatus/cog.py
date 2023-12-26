from discord.ext import commands
from mcstatus import JavaServer
import discord
from discord import app_commands

class MCStatus(commands.Cog, name ="Minecraft Status"):
    """Pings to the given IP Address and displays server status."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    @app_commands.command(
          name= "mcstatus",
          description="Pings to the given IP Address and displays server status."
    )
    async def mcstatus(self, interaction: discord.Interaction, ipaddress: str):
        server = JavaServer.lookup(ipaddress)
        query = server.query()
        latency = server.ping()
        ping = round(latency)
        if query.players.names:
          await interaction.response.send_message(f"`[SYSTEM]` **Players Online:** `{','.join(query.players.names)}`" +  
                      "\n`[SYSTEM]` **Server Ping:** `{0}`ms".format(ping)      
                      )
        else:
         status = server.status()
         if not status.players.sample:
           await interaction.response.send_message("`[SYSTEM]` There are **no** players online!" +  
                        "\n`[SYSTEM]` **Server Ping:** `{0}`ms".format(ping)
                        )
         else:
           await interaction.response.send_message(f"`[SYSTEM]` **Players online:**+ `{', '.join([player.name for player in status.players.sample])}"  +  
                       "\n**`[SYSTEM]` **Server Ping:** `{0}`ms".format(ping)
                       )

    
    
async def setup(bot: commands.Bot):
    await bot.add_cog(MCStatus(bot))