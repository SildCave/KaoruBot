import discord
from discord.ext import tasks, commands

import time

import data_types

class Systems(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        self.mute_loop.start()

    @tasks.loop(seconds=1)
    async def mute_loop(self):
        muted_users = self.bot.database.select(
            table_name="muted_users",
            columns="*",
            where=f"muted = 1"
        )

        for muted_user in muted_users:
            muted_user = data_types.MutedUser(muted_user)
            print(muted_user)
            if muted_user.muted_untill < time.time():
                guild = self.bot.get_guild(muted_user.guild_id)
                member = guild.get_member(muted_user.user_id)
                muted_role = discord.utils.get(guild.roles, name="muted")
                await member.remove_roles(muted_role)
                self.bot.database.update(
                    table_name="muted_users",
                    set=f"muted = 0",
                    where=f"user_id = {muted_user.user_id} AND guild_id = {muted_user.guild_id}"
                )

async def setup(bot):
    await bot.add_cog(Systems(bot))