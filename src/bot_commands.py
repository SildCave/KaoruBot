from discord.ext import commands
from discord import app_commands

import asyncio
import time
import discord

import data_types

class CommandsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def sync(self, ctx):
        print("sync command")
        if ctx.author.id == 534732412090056705:
            self.bot.tree.copy_global_to(guild=ctx.guild)
            await self.bot.tree.sync(guild=ctx.guild)
            await ctx.send('Command tree synced.')
        else:
            await ctx.send('You must be the owner to use this command!')

    @commands.command()
    async def sync_global(self, ctx: commands.Context):
        # sync globally
        if ctx.author.id == 534732412090056705:
            await self.bot.tree.sync()

            await ctx.send(content="Success")

    @app_commands.command(name="selfmute", description="Mute yourself")
    async def selfmute(self, interaction, duration_in_seconds: int):
        if duration_in_seconds < 0:
            await interaction.response.send_message(content="Duration must be positive.", ephemeral=False)
            return
        muted_role = discord.utils.get(interaction.guild.roles, name="muted")

        if muted_role is None:
            await interaction.response.send_message(content="Muted role not found.", ephemeral=False)
            return

        await interaction.user.add_roles(muted_role)
        self.bot.database.insert_or_update(
            table_name="muted_users",
            columns="user_id, guild_id, muted, muted_untill",
            values=f"{interaction.user.id}, {interaction.guild.id}, 1, {time.time() + duration_in_seconds}"
        )

        await interaction.response.send_message(content=f"You are muted for {duration_in_seconds} seconds", ephemeral=False)


    @app_commands.command(name="mute", description="Mute a user")
    async def mute_user(self, interaction, user: discord.User, duration_in_seconds: int):
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message(content="You must be an administrator to use this command.", ephemeral=False)
            return

        if duration_in_seconds < 0:
            await interaction.response.send_message(content="Duration must be positive.", ephemeral=True)
            return

        muted_role = discord.utils.get(interaction.guild.roles, name="muted")

        if muted_role is None:
            await interaction.response.send_message(content="Muted role not found.", ephemeral=True)
            return

        await user.add_roles(muted_role)
        self.bot.database.insert_or_update(
            table_name="muted_users",
            columns="user_id, guild_id, muted, muted_untill",
            values=f"{user.id}, {interaction.guild.id}, 1, {time.time() + duration_in_seconds}"
        )

        await interaction.response.send_message(content=f"{user.mention} is muted for {duration_in_seconds} seconds", ephemeral=False)


    @app_commands.command(name="reaction_stats", description="Get reaction stats")
    async def reaction_stats(self, interaction):
        reactions = self.bot.database.select(
            table_name="reactions",
            columns="*",
            where=f"guild_id = {interaction.guild.id}"
        )

        reaction_stats = {}
        for reaction in reactions:
            reaction = data_types.Reaction(reaction)
            if reaction.user_id == interaction.user.id:
                reaction_stats[reaction.emoji] = reaction_stats.get(reaction.emoji, 0) + 1

        message_embed = discord.Embed(
            title="Reaction Stats",
            description="",
            color=0x00ff00
        )

        for reaction in reaction_stats:
            message_embed.add_field(
                name=reaction,
                value=reaction_stats[reaction],
                inline=True
            )

        await interaction.response.send_message(embed=message_embed, ephemeral=False)


    @app_commands.command(name="register_reaction_for_tracking", description="Add reaction to the tracker")
    async def add_reaction_to_tracker(self, interaction: discord.Interaction, reaction: str, announcement_channel_id: discord.TextChannel):
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message(content="You must be an administrator to use this command.", ephemeral=False)
            return

        self.bot.database.insert_or_update(
            table_name="reaction_tracker",
            columns="guild_id, reactions_announcement_channel_id, tracked_reaction_emoji",
            values=f"{interaction.guild.id}, {announcement_channel_id.id}, '{reaction}'"
        )

        await interaction.response.send_message(content="Reaction added to tracker.", ephemeral=True)


async def setup(bot):
    await bot.add_cog(CommandsCog(bot))