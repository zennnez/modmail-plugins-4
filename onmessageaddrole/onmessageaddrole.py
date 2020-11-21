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

    @commands.group(name="omar", invoke_without_command=True)
    @checks.has_permissions(PermissionLevel.MODERATOR)
    async def omar(self,ctx:commands.Context,*):
        """Assign roles to members when they type in specified channel."""
        await ctx.send_help(ctx.command)
        
    @omar.command(name="add")
    @checks.has_permissions(PermissionLevel.MODERATOR)
    async def omar_add(self, ctx,*, role:discord.Role, channel:discord.TextChannel.id):
        channelroles[channel]=role

    @commands.Cog.listener()
    async def on_message(self, member):
        member = context.author
        for channel in channelroles:
            rg = channelroles.get(channel)
            if role in context.author.roles:
                continue
            else:
                context.author.add_role(rg)


def setup(bot):
    bot.add_cog(OnMessageAddRole(bot))