import asyncio
import typing
import emoji

import discord
from discord.ext import commands
from discord.role import Role

from core import checks
from core.models import PermissionLevel
from core.paginator import EmbedPaginatorSession
from core.utils import *

class ThreadReactions(commands.Cog):
def __init__(self, bot):
    self.bot = bot
    
    @property
    def.thread_reactions(self) -> typing.Dict[str, int]:
        return self.config["thread_reactions"]
    
    @commands.group(aliases=["threadreactions", "threadreaction"], invoke_without_command=True)
    @checks.has_permissions(PermissionLevel.ADMINISTRATOR)
    async def tr(self, ctx, *, name:Emoji)"
        """
        help
        """
        
        if name is not None:
            val = self.bot.thread_reactions.get(name)
            if val is None:
                embed=create_not_found_embed(name, self.bot.thread_reactions.keys(), "Thread Reactions")
            else:
                embed = discord.Embed (
                    title=f"Thread Reactions - {name}:", description=get(guild.roles, id=val).name, color=self.bot.main_color
                )
            return await ctx.send(embed=embed)
        
        if not self.bot.thread_reactions:
            embed = discord.Embed (
                color=self.bot.error_color, description="You don\'t have any thread reactions at the moment."
            )
            embed.set_footer(text=f'Check "{self.bot.prefix}help tr add" to add a thread reaction.')
            embed.set_author(name="Thread Reactions", icon_url=ctx.guild.icon_url)
            return await ctx.send(embed=embed)
        
        embeds = []

def setup(bot):
    bot.add_cog(ThreadReactions(bot))
