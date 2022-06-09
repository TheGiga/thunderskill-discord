import discord
from discord import SlashCommand
from discord.ext.commands import has_permissions

import config
import lib.models
from lib.models import Guild
from lib.utilities import code_to_locale
from lib.utilities.db import db_session


class Admin(discord.Cog):
    def __init__(self, bot):
        self.bot: discord.Bot = bot

    @discord.slash_command(name='help', description='Basic bot info.')
    async def information(self, ctx: discord.ApplicationContext):
        thunder_guild: lib.models.Guild = await lib.models.Guild.get_or_create(ctx.guild)
        lcl = thunder_guild.locale

        loc = lib.code_to_locale(lcl)

        embed = discord.Embed(colour=discord.Colour.embed_background())

        embed.add_field(name='🏓 Client Latency', value=f'{round(self.bot.latency * 1000)}ms')
        embed.add_field(name='📐 Registered Commands', value=str(len(self.bot.commands)))
        embed.add_field(name='🤖 Loaded Cogs', value=str(len(self.bot.cogs)))
        embed.add_field(name=loc.LANGUAGE, value=f"{loc.FLAG} {lcl.upper()}")

        embed.set_thumbnail(url=self.bot.user.avatar.url)

        embed.set_author(name='by gigalegit-#0880', icon_url=config.OWNER_AV, url='https://github.com/TheGiga')

        united_description = ''
        last_cog = ''
        for command in self.bot.commands:
            if type(command) is not SlashCommand:
                continue
            if command.cog.qualified_name != 'Admin':
                if last_cog != command.cog.qualified_name:
                    united_description += f'**{command.cog.qualified_name}**\n'
                last_cog = command.cog.qualified_name
                united_description += f'> `/{command.name}` - ' \
                                      f'{command.description if command.name != "help" else "**THIS COMMAND**"}\n'
            else:
                continue

        embed.description = united_description

        embed.set_footer(text=f"{loc.GUILDS}: {len(self.bot.guilds)}")

        await ctx.respond(embed=embed)

    @has_permissions(administrator=True)
    @discord.slash_command(name='set-language')
    async def set_lang(
            self, ctx: discord.ApplicationContext,
            lang: discord.Option(
                str, name='language', description="Language to set.",
                choices=["🇷🇺", "🇺🇦", "🇬🇧"]
            )
    ):
        thunder_guild: Guild = await Guild.get_or_create(ctx.guild)

        match lang:
            case "🇷🇺":
                lcl = "ru"
            case "🇺🇦":
                lcl = "ua"
            case "🇬🇧":
                lcl = "en"
            case _:
                lcl = "en"

        loc = code_to_locale(lcl)

        thunder_guild.locale = lcl
        db_session.commit()

        await ctx.respond(ephemeral=True, content=f'{loc.FLAG} **{loc.NEW_LANGUAGE_MESSAGE}**')


def setup(bot: discord.Bot):
    bot.add_cog(Admin(bot=bot))
