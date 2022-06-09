import calendar
from datetime import datetime

import discord

import lib.errors
from lib import Squadron
from lib.models import Guild
from lib.utilities import code_to_locale


class SquadronStats(discord.Cog):
    def __init__(self, bot: discord.Bot):
        self.bot = bot

    @discord.slash_command(name='squadron', description='Check Squadron information / Посмотреть информацию о Полке')
    async def squadron(
            self,
            ctx: discord.ApplicationContext,
            tag: discord.Option(
                str, name='nametag',
                description="Tag of Squadron with all symbols. [NAME] / =NAME="
            )
    ):
        thunder_guild: Guild = await Guild.get_or_create(ctx.guild)

        try:
            info = await Squadron.from_name(name=tag)
        except lib.errors.FailedToGetStats:
            return await ctx.respond(
                content=f"**:x: Squadron `{tag}` not found!**",
                ephemeral=True
            )

        await ctx.defer()

        embed = discord.Embed(colour=discord.Colour.embed_background(), title=info.name)

        embed.add_field(name='🕗 AB KPD', value=f'{info.ab_kpd}%')
        embed.add_field(name='🕔 RB KPD', value=f'{info.rb_kpd}%')
        embed.add_field(name='🕚 SB KPD', value=f'{info.sb_kpd}%')

        embed.set_footer(text='by gigalegit-#0880')

        united_description = ''
        for player in info.players:

            united_description += f'`{player.get("nick")}` '

        embed.description = united_description

        view = discord.ui.View()
        btn = discord.ui.Button(
            label="ThunderSkill",
            url=f"https://thunderskill.com/en/squad/{info.name}",
            emoji="🔖"
        )
        view.add_item(btn)

        await ctx.respond(embed=embed, view=view)


def setup(bot: discord.Bot):
    bot.add_cog(SquadronStats(bot=bot))
