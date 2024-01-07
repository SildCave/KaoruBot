import os
import asyncio

import discord
from discord.ext import commands

import database

db = database.Database()
database.create_schema(db)

intents = discord.Intents.default().all()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print("Ready!")

token = os.environ["DISCORD_TOKEN"]


async def main():
    async with bot:
      await bot.load_extension("bot_commands")
      await bot.start(token)

asyncio.run(main())