import asyncio

import discord
from discord.ext import commands
from discord.utils import get

from core import checks
from core.models import PermissionLevel
from core.utils import *

class ThreadReactions(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    thread_reactions = dict()
    global thread_reactions

    @commands.group(invoke_without_command=True)
    @checks.has_permissions(PermissionLevel.SUPPORTER)
    async def tr(self, ctx):
        """
        Creates reactions to thread genesis message for assigning roles.

        When '{prefix}tr' is used by itself, this will retrieve
        a list of reaction roles currently assigned.

        To add reactions to thread:
        - '{prefix}thr add'
        """

        if not thread_reactions:
            embed=discord.Embed(
                colour=self.bot.error_color,
                description="You dont have any thread reaction roles at the moment"
            )
            embed.set_footer(text=f"Check'{self.bot.prefix}help tr add' to add a reaction role.")
            return await ctx.send(embed=embed)

        embed=discord.Embed(
            colour=self.bot.main_color,
            description="Thread reactions not empty"
        )
        embed.set_footer(text="Work in process. Will implement listing soon.")
        return await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(ThreadReactions(bot))