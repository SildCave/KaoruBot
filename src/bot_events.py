from discord.ext import commands
from discord import app_commands

import logging

async def handle_reaction_role_add(self, payload):
    message_id = payload.message_id
    guild_id = payload.guild_id
    print(message_id)
    registered_reactions = self.bot.database.select(
        table_name="roles",
        columns="*",
        where=f"message_id = {message_id}"
    )

    for reaction in registered_reactions:
        reaction_emoji = reaction[1]
        reaction_role_id = reaction[0]
        if reaction_emoji.strip() == str(payload.emoji).strip():
            print("reaction role add")
            guild = self.bot.get_guild(guild_id)
            member = guild.get_member(payload.user_id)
            role = guild.get_role(reaction_role_id)
            await member.add_roles(role)

async def handle_reaction_role_remove(self, payload):
    message_id = payload.message_id
    guild_id = payload.guild_id
    print(message_id)
    registered_reactions = self.bot.database.select(
        table_name="roles",
        columns="*",
        where=f"message_id = {message_id}"
    )

    for reaction in registered_reactions:
        reaction_emoji = reaction[1]
        reaction_role_id = reaction[0]
        if reaction_emoji.strip() == str(payload.emoji).strip():
            print("reaction role remove")
            guild = self.bot.get_guild(guild_id)
            member = guild.get_member(payload.user_id)
            role = guild.get_role(reaction_role_id)
            await member.remove_roles(role)

class EventsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        logging.info("Bot is ready.")
        print("Bot is ready.")


    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        # Track reactions
        print("reaction add")
        emoji = payload.emoji
        user_id = payload.user_id
        message_id = payload.message_id
        channel_id = payload.channel_id
        guild_id = payload.guild_id

        self.bot.database.insert_or_update(
            table_name="reactions",
            columns="reaction_name, emoji, guild_id, message_id, channel_id, user_id",
            values=f"'{emoji.name}', '{emoji}', {guild_id}, {message_id}, {channel_id}, {user_id}"
        )

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        await handle_reaction_role_remove(self, payload)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        # Send info about subscribed reactions
        await handle_reaction_role_add(self, payload)
        print("reaction add")
        channel = await self.bot.fetch_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        user = await self.bot.fetch_user(payload.user_id)

        emoji_name = payload.emoji.name
        user_id = payload.user_id
        message_id = payload.message_id
        channel_id = payload.channel_id
        guild_id = payload.guild_id


        subscribed_reactions = self.bot.database.select(
            table_name="reaction_tracker",
            columns="*",
            where=f"guild_id = {guild_id}"
        )

        for reaction in subscribed_reactions:
            reaction_emoji = reaction[2]
            reaction_guild_id = reaction[0]
            if (reaction_emoji == emoji_name.strip()) and (reaction_guild_id == guild_id):
                reaction_announcement_channel = await self.bot.fetch_channel(reaction[1])
                await reaction_announcement_channel.send(f"{user.mention} reacted with {emoji_name} to {message.jump_url}")


async def setup(bot):
    await bot.add_cog(EventsCog(bot))