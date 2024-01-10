from humanfriendly import format_timespan
import discord

class MuteCommandResponse(object):
    def __init__(self, duration_seconds, user):
        self.duration_seconds = duration_seconds
        self.user = user

    def to_embed(self):
        embed = discord.Embed(
            title="",
            description=f"<@{self.user.id}> has been muted for **{format_timespan(self.duration_seconds)}**.",
            color=discord.Color.red()
        )
        return embed

class SelfMuteResponse(object):
    def __init__(self, duration_seconds, user):
        self.duration_seconds = duration_seconds
        self.user = user

    def to_embed(self):
        embed = discord.Embed(
            title="",
            description=f"You have muted yourself for **{format_timespan(self.duration_seconds)}**. NOW GET TO WORK!",
            color=discord.Color.blurple()
        )
        return embed
    
class UnmuteCommandResponse(object):
    def __init__(self, user):
        self.user = user

    def to_embed(self):
        embed = discord.Embed(
            title="",
            description=f"<@{self.user.id}> has been **unmuted**.",
            color=discord.Color.green()
        )
        return embed
