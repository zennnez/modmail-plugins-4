import asyncio
import emoji

import discord
from discord.ext import commands
from discord.utils import get

from core import checks
from core.models import PermissionLevel
from core.config import *
from core.utils import *

class RoleCO(commands.RoleConverter):
    async def convert(self, ctx, argument):
        return discord,Role()
    raise commands.BadArgument("Unknown role")

class EmojiCO(commands.PartialEmojiConverter):
    async def convert(self, ctx, argument):
        if argument in emoji.UNICODE_EMOJI:
            return discord.PartialEmoji(name=argument, animated=False)
        else:
            return discord.PartialEmoji()
        raise commands.BadArgument("Unknown emoji")


class ThreadReactions(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    global thread_reactions
    thread_reactions = dict()

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
                color=self.bot.error_color,
                description="You dont have any thread reaction roles at the moment"
            )
            embed.set_footer(text=f"Check'{self.bot.prefix}help tr add' to add a reaction role.")
            return await ctx.send(embed=embed)

        embed=discord.Embed(
            color=self.bot.main_color,
            description="Thread reactions not empty"
        )
        embed.set_footer(text="Work in process. Will implement listing soon.")
        return await ctx.send(embed=embed)

    @tr.command(name="add")
    @checks.has_permissions(PermissionLevel.ADMINISTRATOR)
    async def tr_add(self, ctx, name=EmojiCO, *, value=RoleCO):
        """
        Add a reaction role.

        To add a reaction, do:
        - '{prefix}tr add emoji role'
        """

        emote = name.name if name.id is None else str(name.id)
        role = str(value.id)

        for key in thread_reactions:
            if thread_reactions[key] == role:
                await thread_reactions.pop(key)
                break

        thread_reactions[emote] = role
        embed=discord.Embed(
            title="Reaction role added",
            color=self.bot.main_color,
            description=f"{str(name)} is successfully assigned to {str(value)}."
        )
        return await ctx.send(embed=embed)

    @tr.command(name="remove", aliases=["del", "delete"])
    @checks.has_permissions(PermissionLevel.ADMINISTRATOR)
    async def tr_remove(self, ctx, *, name=EmojiCO):
        """
        Removes a reaction role.

        To remove a reaction, do:
        - '{prefix}tr remove emoji'
        """

        emote = name.name if name.id is None else str(name.id)

        if emote in thread_reactions:
            await thread_reactions.pop(emote)
            embed = discord.Embed(
                title="Reaction role removed",
                color=self.bot.main_color,
                description=f"{str(name)}has been successfully unassigned."
            )
            return await ctx.send(embed=embed)

        embed = discord.Embed(
            color=self.bot.error_color,
            description=f"{str(name)} is already not assigned to a reaction role."
        )
        return await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(ThreadReactions(bot))