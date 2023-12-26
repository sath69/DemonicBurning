from discord.ext import commands
import coc
import discord
from discord import app_commands




class WarStatus(commands.Cog, name ="War Status"):
  """Shows clan war status of the clan."""

  def __init__(self, bot: commands.Bot):
        self.bot = bot
    
  @app_commands.command(
          name="warstatus",
          description="Shows clan war status of the clan."
  )
  async def warstatus(self, interaction: discord.Interaction):

    e = discord.Embed(colour=discord.Colour.blue())

    try:
        war = await self.bot.coc_client.get_current_war("#2P9U8C9GJ")
    except coc.PrivateWarLog:
        return await interaction.response.send_message("Clan has a private war log!")

    if war is None:
        return await interaction.response.send_message("Clan is in a strange CWL state!")
    

    e.add_field(name="War State:", value=war.state, inline=False)

    if war.end_time:

        hours, remainder = divmod(int(war.end_time.seconds_until), 3600)
        minutes, seconds = divmod(remainder, 60)
        if war.end_time.seconds_until < 0:
            e.add_field(name="War End Time:",
                        value="`War has ended.`",
                        inline=False)
        else:
             e.add_field(name="War End Time:",
                    value=f"`{hours}` hours `{minutes}` minutes `{seconds}` seconds",
                    inline=False)

        e.add_field(name = "Clan:", value=f"**{war.clan.name}**\n" f"`{war.clan.tag}`\n")
        e.add_field(
            name="Opponent:",
            value=f"**{war.opponent.name}**\n" f"`{war.opponent.tag}`", inline=False)
        e.add_field(name="Result | Status:", 
                    value=f"`{war.status}`", inline= False)
        e.add_field(name="Score:",
                    value=f"Clan: **{war.clan.name}:** `{war.clan.stars}` stars\nOpponent: **{war.opponent.name}:** `{war.opponent.stars}` stars",inline= False)
        e.add_field(name="Attackers per team:",
                    value=f"`{war.team_size}`")
  
 
    await interaction.response.send_message(embed=e)
    
async def setup(bot: commands.Bot):
    await bot.add_cog(WarStatus(bot))
