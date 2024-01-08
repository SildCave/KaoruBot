from discord.ext import commands
from discord import app_commands

import discord

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

    @app_commands.command(name="ss", description="Get reaction stats")
    async def reaction_stats(self, interaction):
        reactions = self.bot.database.select(
            table_name="reactions",
            columns="*",
            where=f"guild_id = {interaction.guild.id}"
        )

        message_embed = discord.Embed(
            title="Reaction Stats",
            description="",
            color=0x00ff00
        )
        for reaction in reactions:
            message_embed.add_field(
                name=reaction[0],
                value=reaction[1],
                inline=False
            )

        await interaction.response.send_message(
            embed=message_embed,
            ephemeral=False
        )

async def setup(bot):
    await bot.add_cog(CommandsCog(bot))