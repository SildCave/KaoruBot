from discord.ext import commands
from discord import app_commands

import logging

class EventsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        logging.info("Bot is ready.")
        print("Bot is ready.")

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        channel = await self.bot.fetch_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        user = await self.bot.fetch_user(payload.user_id)
        emoji = payload.emoji
        print(payload)
        if message.channel.id == 1193225059670687744:
            await channel.send(f"no fun allowed {user.mention}")

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        # Track reactions
        
        channel = await self.bot.fetch_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        user = await self.bot.fetch_user(payload.user_id)

        emoji = payload.emoji
        user_id = payload.user_id
        message_id = payload.message_id
        channel_id = payload.channel_id
        guild_id = payload.guild_id

        self.bot.database.insert(
            table_name="reactions",
            columns="reaction_name, emoji, guild_id, message_id, channel_id, user_id",
            values=f"'{emoji.name}', '{emoji}', {guild_id}, {message_id}, {channel_id}, {user_id}"
        )



async def setup(bot):
    await bot.add_cog(EventsCog(bot))