import os
import asyncio
import logging
import logging.handlers
import sys

import discord
from discord.ext import commands

import database

db = database.Database()
database.create_schema(db)

logger = logging.getLogger()
logger.setLevel(logging.INFO)
logging.getLogger('discord.http').setLevel(logging.INFO)

handler = logging.handlers.RotatingFileHandler(
    filename='discord.log',
    encoding='utf-8',
    maxBytes=32 * 1024 * 1024,  # 32 MiB
    backupCount=5,  # Rotate through 5 files
)
dt_fmt = '%Y-%m-%d %H:%M:%S'
formatter = logging.Formatter('[{asctime}] [{levelname:<8}] {name}: {message}', dt_fmt, style='{')
handler.setFormatter(formatter)
#logger.addHandler(stdout_handler)
logger.addHandler(handler)


intents = discord.Intents.default().all()
intents.members = True
bot = commands.Bot(command_prefix="!", intents=intents)
bot.database = db

token = os.environ["DISCORD_TOKEN"]


async def main():
    async with bot:
        await bot.load_extension("bot_commands")
        await bot.load_extension("bot_events")
        await bot.start(token)

asyncio.run(main())