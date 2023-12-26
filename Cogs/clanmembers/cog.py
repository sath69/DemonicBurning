from discord.ext import commands
import discord
from discord import app_commands
import coc



class ClanMembers(commands.Cog, name ="clanmembers"):
    """Retrieves a clan members list from the clan."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    @app_commands.command(
          name= "clanmembers",
          description="Retrieves a clan members list from the clan."
    )
    async def clanmembers(self,interaction: discord.Interaction):

     clan = await self.bot.coc_client.get_clan("#2P9U8C9GJ")

     member = ""
     for i, a in enumerate(clan.members, start=1):
        member += f"\n`{i}.` *{a.name}*\n**Player Tag & Role:**\n`{a.tag}`,**{a.role}**\n"

     embed = discord.Embed(colour=discord.Colour.red(),title=f"Members of {clan.name}", description=member)
     embed.set_thumbnail(url=clan.badge.url)
     embed.set_footer(text=f"Total Members - {clan.member_count}/50")
     await interaction.response.send_message(embed=embed)

    

    
async def setup(bot: commands.Bot):
    await bot.add_cog(ClanMembers(bot))