import asyncio
import emoji
import typing
from itertools import takewhile, zip_longest

import discord
from discord.ext import commands
from discord.utils import get

from core import checks
from core.models import PermissionLevel
from core.config import *
from core.utils import *

class EmojiCO(commands.PartialEmojiConverter):
    async def convert(self, ctx, argument):
        if argument in emoji.UNICODE_EMOJI:
            return discord.PartialEmoji(name=argument, animated=False)
        raise commands.BadArgument("Unknown emoji")

EmojiOBJ = typing.Union[discord.PartialEmoji, discord.Emoji, EmojiCO]

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

        embeds = []

        def tr_format_description(names, values):
            return "\n".join(
                ": ".join(a, b)
                for emote, role in enumerate(takewhile(names, values))
            )

        for names, values in enumerate(zip_longest(*(iter(sorted(thread_reactions))) * 15)):
            description = tr_format_description(names, values)
            embed = discord.Embed(title="Thread Reaactions", color=self.bot.main_color, description=description)
            embeds.append(embed)

        session = EmbedPaginatorSession(ctx, *embeds)
        await session.run()

    @tr.command(name="add")
    @checks.has_permissions(PermissionLevel.ADMINISTRATOR)
    async def tr_add(self, ctx, name:EmojiOBJ, *, value:discord.Role):
        """
        Add a reaction role.

        To add a reaction, do:
        - '{prefix}tr add emoji role'
        """

        emote = name.name if name.id is None else str(name.id)
        role = str(value.id)

        for key in thread_reactions:
            if thread_reactions[key] == role:
                thread_reactions.pop(key)
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
    async def tr_remove(self, ctx, *, name:EmojiOBJ):
        """
        Removes a reaction role.

        To remove a reaction, do:
        - '{prefix}tr remove emoji'
        """

        emote = name.name if name.id is None else str(name.id)

        if emote in thread_reactions:
            thread_reactions.pop(emote)
            embed = discord.Embed(
                title="Reaction role removed",
                color=self.bot.main_color,
                description=f"{str(name)} has been successfully unassigned."
            )
            return await ctx.send(embed=embed)

        embed = discord.Embed(
            color=self.bot.error_color,
            description=f"{str(name)} is already not assigned to a reaction role."
        )
        return await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(ThreadReactions(bot))