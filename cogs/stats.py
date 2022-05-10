import calendar
from datetime import datetime

import discord

import lib.errors
from lib import Player
from lib.models import Guild
from lib.utilities import rank_to_colour, code_to_locale


class Core(discord.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(
        name='player',
        description="Check player statistics by Nickname / Проверить статистику поьзователя по Никнейму"
    )
    async def player_command(
            self,
            ctx: discord.ApplicationContext,
            nickname: discord.Option(
                str, name='nick',
                description="Player Nickname / Никнейм игрока"
            ),
            game_type: discord.Option(
                str, name='gamemode',
                description="Game mode to check stats from / Игровой режим по которому будет выведена статистика",
                choices=["RB", "AB", "SB"]
            ) = "AB"
    ):
        thunder_guild: Guild = await Guild.get_or_create(ctx.guild)

        try:
            info = await Player.from_nickname(nickname=nickname)
        except lib.errors.FailedToGetStats:
            return await ctx.respond(
                content=f"**:x: Игрок `{nickname}` не найден!**",
                ephemeral=True
            )

        match game_type:
            case "AB":
                data = info.arcade
            case "RB":
                data = info.realistic
            case "SB":
                data = info.simulator
            case _:
                data = info.arcade

        loc = code_to_locale(code=thunder_guild.locale)

        embed = discord.Embed(
            title=f"{info.nickname} - {info.rank}",
            colour=rank_to_colour(info.rank),
            timestamp=discord.utils.utcnow()
        )
        embed.description = f"{loc.STATISTICS_TYPE.format(game_type)}" \
                            f"{loc.LAST_UPDATE} <t:{calendar.timegm(datetime.timetuple(info.last_update))}:R>"

        embed.add_field(name="🕗 KPD", value=f"{data.get('kpd')}", inline=False)
        embed.add_field(
            name='⚔️ W/Overall | Winrate%',
            value=f"{data.get('win')}/{data.get('mission')} **|** `{data.get('winrate')}%`"
        )

        embed.add_field(
            name='💀 KD | KB',
            value=f"{data.get('kd')} **|** {data.get('kb')} "
        )

        embed.set_footer(text='by gigalegit-#0880')

        view = discord.ui.View()
        btn = discord.ui.Button(
            label="ThunderSkill",
            url=f"https://thunderskill.com/en/stat/{info.nickname}",
            emoji="🔖"
        )
        view.add_item(btn)

        await ctx.respond(embed=embed, view=view)


def setup(bot: discord.Bot):
    bot.add_cog(Core(bot=bot))
