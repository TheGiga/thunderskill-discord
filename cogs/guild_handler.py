import discord
from discord import Forbidden
from lang import en

from lib.models import Guild


class Handler(discord.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.Cog.listener()
    async def on_guild_join(self, guild: discord.Guild):
        await Guild.get_or_create(guild)

        try:
            embed = discord.Embed(title='Thunder Skill', color=discord.Color.embed_background())
            embed.description = en.default_description

            embed.set_footer(text='by gigalegit-#0880')

            await guild.system_channel.send(embed=embed)
        except Forbidden:
            pass


def setup(bot: discord.Bot):
    bot.add_cog(Handler(bot=bot))
