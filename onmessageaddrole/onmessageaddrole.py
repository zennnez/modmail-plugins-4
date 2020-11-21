import asyncio
import re

import discord
from discord.ext import commands
from discord.role import Role

from core import checks
from core.models import PermissionLevel

class OnMessageAddRole(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        channelroles = []

    @commands.group(name="onmessageaddrole", alisases=["omar"], invoke_without_command=True)
    @checks.has_permissions(PermissionLevel.MODERATOR)
    async def onmessageaddrole(self,ctx:commands.Context):
        """Assign roles to members when they type in specified channel."""
        await ctx.send_help(ctx.command)
        
    @onmessageaddrole.command(name="add")
    @checks.has_permissions(PermissionLevel.MODERATOR)
    async def omar_add(self, ctx,*, role:discord.Role, channel:discord.TextChannel.id):
        channelroles[channel]=role

    @commands.Cog.listener()
    async def on_message(message):
        for channel in channelroles:
            if role in message.author.roles:
                continue
            else:
                context.author.add_role(role)


def setup(bot):
    bot.add_cog(OnMessageAddRole(bot))
