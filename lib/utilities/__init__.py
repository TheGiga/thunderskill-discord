from typing import Union

from lang import ua, ru, en
from .cog_loader import loader as cog_loader

import discord


def code_to_locale(code: str):
    match code:
        case "ru":
            loc = ru
        case "en":
            loc = en
        case "ua":
            loc = ua
        case _:
            loc = en

    return loc


def rank_to_colour(rank: str) -> Union[None, discord.Color]:
    colours = {
        "Doesn`t play": discord.Color.dark_gray,
        "Не играет": discord.Color.dark_gray,
        "Terrible player": discord.Color.from_rgb(205, 51, 51),
        "Ужасный игрок": discord.Color.from_rgb(205, 51, 51),
        "Bad player": discord.Color.from_rgb(215, 121, 0),
        "Плохой игрок": discord.Color.from_rgb(215, 121, 0),
        "Average player": discord.Color.from_rgb(234, 201, 0),
        "Средний игрок": discord.Color.from_rgb(234, 201, 0),
        "Above average": discord.Color.from_rgb(131, 174, 35),
        "Выше среднего игрок": discord.Color.from_rgb(131, 174, 35),
        "Good player": discord.Color.from_rgb(76, 118, 46),
        "Хороший игрок": discord.Color.from_rgb(76, 118, 46),
        "Excellent player": discord.Color.from_rgb(74, 146, 183),
        "Превосходный игрок": discord.Color.from_rgb(74, 146, 183),
        "Outstanding player": discord.Color.from_rgb(153, 84, 187),
        "Уникальный игрок": discord.Color.from_rgb(153, 84, 187)
    }

    if colours.get(rank) is None:
        colour = discord.Colour.embed_background()
    else:
        colour = colours.get(rank)

    return colour
