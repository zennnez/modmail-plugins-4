import asynchio
import re

import discord
from discord.ext import commands

from core import checks
from core.models import PermissionLevel
from core.paginator import EmbedPaginatorSession

@property
def thread_react_roles(self) -> typing.Dict[str, str]:
    return self.config["thread_react_roles"]

class Thread_ReactRoles(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.db = bot.plugin_db.get_partition(self)

    @commands.group(name="threadreactrole", aliases=["trr"], invoke_without_command=True)
    @checks.has_permissions(PermissionLevel.ADMINISTRATOR)
    async def threadreactrole(self, ctx, *, name: str.lower = None):
        """
        Creates tickets with reactions, allowing users to assign roles to ticket recipients.
        """

        if name is not None:
            val = self.bot.thread_react_roles.get(name)
            if val is None:
                embed = create_not_found_embed(name, self.bot.thread_react_roles.keys(), "Thread Reactions")
            else:
                embed = discord.Embed(
                    title=f'Reactions - "{name}":', description=val, color=self.bot.main_color
                )
            return await ctx.send(embed=embed)

        if not self.bot.thread_react_roles:
            embed = discord.Embed(
                color=self.bot.error_color, description="You dont have any thread reactions at the moment."
            )
            embed.set_footer(text=f'Check "{self.bot.prefix}help trr add" to add a thread reaction.')
            embed.set_author(name="Thread React Roles", icon_url=ctx.guild.icon_url)
                return await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Thread_ReactRoles(bot))
