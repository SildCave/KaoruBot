from discord.ext import commands
from discord import app_commands

class CommandsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def sync(self, ctx):
        print("sync command")
        if ctx.author.id == 534732412090056705:
            await self.bot.tree.sync(guild=ctx.guild)
            await ctx.send('Command tree synced.')
        else:
            await ctx.send('You must be the owner to use this command!')

    @app_commands.command(name="ss", description="ss")
    async def ss(self, interaction):
        await interaction.response.send_message("ss!")

async def setup(bot):
    await bot.add_cog(CommandsCog(bot))