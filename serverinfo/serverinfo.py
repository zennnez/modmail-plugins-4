import asyncio

import discord
from discord.ext import commands
from discord.utils import get

from core import checks
from core.models import PermissionLevel

class ServerInfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @checks.has_permissions(PermissionLevel.OWNER)
    async def serversbasic(self, ctx, *):
        for guild in bot.guilds:
            await ctx.send(content=f"{str(guild.id)} | {str(guild.name)}")
        return await ctx.send(context="done")

    @commands.command()
    @checks.has_permissions(PermissionLevel.OWNER)
    async def channelnames(self, ctx, *, guild):
        for channel in guild.channel:
            await ctx.send(content=f"{str(channel.id)} | {str(channel.name)}")
        return await ctx.send(context="done")

def setup(bot):
    bot.add_cog(ServerInfo(bot))
