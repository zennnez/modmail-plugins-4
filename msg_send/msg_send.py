import asyncio

import discord
from discord.ext import commands

from core import checks
from core.models import PermissionLevel

class MsgSend(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(invoke_without_command = True)
    @checks.has_permissions(PermissionLevel.OWNER)
    async def msgsend(self, ctx: commands.Context):
        """
        Lets Modmail sends messge to the server.
        """
        await ctx.send_help(ctx.command)

    @msgsend.command(name="add")
    @checks.has_permissions(PermissionLevel.OWNER)
    async def msgsend_add(self, ctx, channel: discord.TextChannel, *, message: str):
        """
        Sends a message to a channel through Modmail.
        """

        await channel.send(content=message)

def setup(bot):
    bot.add_cog(MsgSend(bot))
