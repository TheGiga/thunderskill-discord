import os
import discord
import art
from dotenv import load_dotenv
from lib.utilities import cog_loader
from lib.utilities.db import Base, engine

load_dotenv()

bot_instance = discord.Bot(intents=discord.Intents.default())


@bot_instance.event
async def on_ready():
    art.tprint("TS READY")


if __name__ == "__main__":
    from lib.models import Guild
    Base.metadata.create_all(bind=engine)

    cog_loader(bot_instance=bot_instance)
    bot_instance.run(os.getenv("TOKEN"))
