import asynchio
import emoji

import discord
from discord.ext import commands

from core import checks
from core.models import PermissionLevel, getLogger
from core.paginator import EmbedPaginatorSession
from core.thread import Thread

class thread_reactrole(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @property
    def thread_react_role(self) -> typing.Dict[str, str]:
        return self.config["thread_react_role"]

    @commands.group(name="threadreactrole", aliases=["trr"], invoke_without_command=True)
    @checks.has_permissions(PermissionLevel.ADMINISTRATOR)
    async def threadreactrole(self, ctx, *, name: str.lower = None):
        """ 
        Assigns roles to thread recipents using reactions in thread messages.
        When `{prefix}trr` is used by itself, this will retrieve
        a list of reactions that are currently set. 
        To create a reaction:
        - `{prefix}trr add emote role`
        """

        if name is not None:
            val = self.bot.thread_react_role.get(name)
            if val is None:
                embed = create_not_found_embed(name, self.bot.thread_react_role.keys(), "Thread Reactions")
            else:
                embed = discord.Embed(
                    title=f'Thread Reactions - "{name}":"{key}"', description=val, color=self.bot.main_color
                )
            return await ctx.send(embed=embed)

        if not self.bot.snippets:
            embed = discord.Embed(
                color=self.bot.error_color, description="You dont have any reactions at the moment."
            )
            embed.set_footer(text=f'Check "{self.bot.prefix}help trr add" to add a reaction.')
            embed.set_author(name="Thread Reactons", icon_url=ctx.guild.icon_url)
            return await ctx.send(embed=embed)

        embeds = []

    """@commands.Cog.listener()
    async def on_message(self, message):
        print(message.content)"""

def setup(bot):
    bot.add_cog(thread_reactrole(bot))
