from discord.ext import commands
import discord
import coc
from discord import app_commands


class ClanInfo(commands.Cog, name ="claninfo"):
  """Retrieves clan information."""

  def __init__(self, bot: commands.Bot):
        self.bot = bot
    
  @app_commands.command(
          name = "claninfo",
          description="Retrieves clan information."
  )
  async def claninfo(self, interaction: discord.Interaction):

    clan: coc.Clan = await self.bot.coc_client.get_clan("#2P9U8C9GJ")
   

    if clan.public_war_log is False:
        log = "Private"
    else:
        log = "Public"

    e = discord.Embed(colour=discord.Colour.green())

    e.set_thumbnail(url=clan.badge.url)
    e.add_field(name="Clan Name",
                value=f"{clan.name}\n`({clan.tag})`\n[Open in game]({clan.share_link})",
                inline=False)
    e.add_field(name="Clan Level", value=clan.level, inline=False)
    e.add_field(name="Description", value=clan.description, inline=False)
    e.add_field(name="Leader", value=clan.get_member_by(
        role=coc.Role.leader), inline=False)
    e.add_field(name="Clan Type", value=clan.type, inline=False)
    e.add_field(name="Location", value=clan.location, inline=False)
    e.add_field(name="Total Clan Trophies", value=clan.points, inline=False)
    e.add_field(name="Total Clan Builder Base Trophies",
                value=clan.builder_base_points, inline=False)
    e.add_field(name="WarLog Type", value=log, inline=False)
    e.add_field(name="Required Trophies",
                value=clan.required_trophies, inline=False)
    e.add_field(name="War Win Streak", value=clan.war_win_streak, inline=False)
    e.add_field(name="War Frequency", value=clan.war_frequency, inline=False)
    e.add_field(name="Clan War League Rank",
                value=clan.war_league, inline=False)
    e.add_field(name="Clan Labels", value="\n".join(
        label.name for label in clan.labels), inline=False)
    e.add_field(name="Member Count",
                value=f"{clan.member_count}/50", inline=False)
    e.add_field(
        name="Clan Record",
        value=f"Won - {clan.war_wins}\nLost - {clan.war_losses}\n Draw - {clan.war_ties}",
        inline=False
    )

    frame = ""
    for district in clan.capital_districts:
        frame += (f"`{f'{district.name}:':<20}` `{district.hall_level:<15}`\n")

    e2 = discord.Embed(colour=discord.Colour.green(), description=frame,
                       title="Capital Districts")

    await interaction.response.send_message(embeds=[e, e2])
     
    
async def setup(bot: commands.Bot):
    await bot.add_cog(ClanInfo(bot))