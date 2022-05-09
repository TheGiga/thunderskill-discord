import os
import discord
import art
from dotenv import load_dotenv

load_dotenv()

bot_instance = discord.Bot(intents=discord.Intents.default())


@bot_instance.event
async def on_ready():
    art.tprint("TS READY")


if __name__ == "__main__":
    bot_instance.load_extension("cogs.stats")
    bot_instance.run(os.getenv("TOKEN"))
