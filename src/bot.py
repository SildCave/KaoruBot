import os

import discord
from discord import app_commands
from discord.ext import commands

import database

db = database.Database()
database.create_schema(db)

intents = discord.Intents.default().all()
bot = commands.Bot(command_prefix="!", intents=intents)


@bot.tree.command(name="ssss", description="sss")
async def ssss(interaction):
    await interaction.response.send_message("sssss!")

@bot.event
async def on_ready():
    print("Ready!")

@bot.command()
async def sync(ctx):
    print("sync command")
    if ctx.author.id == 534732412090056705:
        await bot.tree.sync()
        await ctx.send('Command tree synced.')
    else:
        await ctx.send('You must be the owner to use this command!')

token = os.environ["DISCORD_TOKEN"]
bot.run(token)