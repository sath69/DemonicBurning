from discord.ext import commands
import coc
import discord
from coc import utils
from discord import app_commands



class PlayerInfo(commands.Cog, name ="Player Info"):
  """Retrieves player info from the Clash of Clans API"""

  def __init__(self, bot: commands.Bot):
        self.bot = bot
    
  @app_commands.command(
          name= "playerinfo",
          description="Retrieves player info from the Clash of Clans API"
  )
  async def playerinfo(self, interaction: discord.Interaction, player_tag: str):
    if not utils.is_valid_tag(player_tag):
        await interaction.response.send_message("You didn't give me a proper tag!")
        return

    try:
        player = await self.bot.coc_client.get_player(player_tag)
    except coc.NotFound:
        await interaction.response.send_message("This player doesn't exist!")
        return

    frame = ''
    if player.town_hall > 11:
        frame += f"`{'TH Weapon LvL:':<15}` `{player.town_hall_weapon:<15}`\n" 
    role = player.role if player.role else 'None'
    clan = player.clan.name if player.clan else 'None'
    frame += (
        f"`{'TH LvL:':<15}` `{player.town_hall:<15}`\n"
        f"`{'Name:': <15}` `{player.name:<15}`\n"
        f"`{'Role:':<15}` `{role:<15}`\n"
        f"`{'Player Tag:':<15}` `{player.tag:<15}`\n"
        f"`{'Current Clan:':<15}` `{clan:<15.15}`\n"
        f"`{'League:':<15}` `{player.league.name:<15}`\n"
        f"`{'Trophies:':<15}` `{player.trophies:<15}`\n"
        f"`{'Best Trophies:':<15}` `{player.best_trophies:<15}`\n"
        f"`{'War Stars:':<15}` `{player.war_stars:<15}`\n"
        f"`{'Attack Wins:':<15}` `{player.attack_wins:<15}`\n"
        f"`{'Defense Wins:':<15}` `{player.defense_wins:<15}`\n"
        f"`{'Capital Contributions':<15}` `{player.clan_capital_contributions:<15}`\n"
    )
    e = discord.Embed(colour=discord.Colour.blurple(),
                      description=frame)
    e.set_thumbnail(url=player.clan.badge.url)
    await interaction.response.send_message(embed=e)
    
    
async def setup(bot: commands.Bot):
    await bot.add_cog(PlayerInfo(bot))