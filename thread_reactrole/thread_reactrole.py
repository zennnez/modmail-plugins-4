import asyncio
import emoji
import re
import typing

import discord
from discord.ext import commands

from core import checks
from core.models import PermissionLevel
from core.paginator import EmbedPaginatorSession

class UnicodeEmoji(commands.Converter):
    async def convert(self, ctx, argument):
        if argument in emoji.UNICODE_EMOJI:
            return discord.PartialEmoji(name=argument, animated=False)
        raise commands.BadArgument('Unknown emoji')

Emoji = typing.Union[discord.PartialEmoji, discord.Emoji, UnicodeEmoji, str]
role_dictionary = {}
thread_initialMessage=0

class Thread_ReactRoles(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.db = bot.plugin_db.get_partition(self)

    @commands.group(name="threadreactrole", aliases=["trr"], invoke_without_command=True)
    @checks.has_permissions(PermissionLevel.ADMINISTRATOR)
    async def threadreactrole(self, ctx: commands.Context):
        """
        Creates tickets with reactions, allowing users to assign roles to ticket recipients.
        """
        await ctx.send_help(ctx.command)
    
    @threadreactrole.command(name="list")
    @checks.has_permissions(PermissionLevel.ADMINISTRATOR)
    async def threadreactrole_list(
        self,
        ctx,
        emoji = Emoji
        ):
        """
        Lists reaction roles assigned.
        """
        await ctx.send_help(ctx.command)
        
        if emoji is not None:
            val = self.bot.snippets.get(emoji)
            if val is None:
                embed = create_not_found_embed(emoji, role_dictionary.keys(), "Reactions")
            else:
                embed = discord.Embed(
                    title=f'Reaction - "{emoji}":', description=val, color=self.bot.main_color
                )
            return await ctx.send(embed=embed)

        if not role_dictionary:
            embed = discord.Embed(
                color=self.bot.error_color, description="You don't have any reactions assigned at the moment."
            )
            embed.set_footer(text=f'Check "{self.bot.prefix}trr add" to add a reaction.')
            embed.set_author(name="Reactions", icon_url=ctx.guild.icon_url)
            return await ctx.send(embed=embed)

            embeds = []

        for i, names in enumerate(zip_longest(*(iter(sorted(role_dictionary)),) * 15)):
            description = format_description(i, emoji)
            embed = discord.Embed(color=self.bot.main_color, description=description)
            embed.set_author(name="Reactions", icon_url=ctx.guild.icon_url)
            embeds.append(embed)

        session = EmbedPaginatorSession(ctx, *embeds)
        await session.run()

    @threadreactrole.command(name="add", usage="[emoji] [role]")
    @checks.has_permissions(PermissionLevel.ADMINISTRATOR)
    async def threadreactrole_add(
        self, 
        ctx, 
        emoji: Emoji, 
        role: discord.Role
    ):
        """
        Assigns a role to an emote for tickets.
        """
        emote = emoji.name if emoji.id is None else str(emoji.id)
        role_dictionary = {emote: role.id}
            
        await ctx.send("Reaction role added.")
    
    @threadreactrole.command(name="remove", usage="[emoji]")
    @checks.has_permissions(PermissionLevel.ADMINISTRATOR)
    async def threadreactrole_remove(
        self,
        ctx,
        emoji: Emoji
    ):
        """
        Removes the role from the emote for tickets.
        """

        emote = emoji.name if emoji.id is None else str(emoji.id)
        role_dictionary.pop(emote)

        await ctx.send("Reaction role removed.")
        
    @commands.Cog.listener()
    async def reaction_add(
        self,
        ctx,
        emoji: Emoji,
        msg: thread_initialMessage
    ):
        if self.bot.modmail_guild.create_text_channel:
            for channel in ctx.thread:
                fetchMessage = await channel.history(limit=1, oldest_first=True)
                thread_initialMessage = fetchMessage

                role_dictionary.get(emoji)
                for emoji in role_dictionary:
                    await self.bot.add_reaction(msg, emoji)

            if channel in self.bot.main_category.channels >1:
                for channel in self.bot.main_category.channels:
                    fetchMessage = await channel.history(limit=1, oldest_first=True)
                    thread_initialMessage = fetchMessage

                    role_dictionary.get(emoji)
                    for emoji in role_dictionary:
                        await self.bot.add_reaction(msg, emoji)

def setup(bot):
    bot.add_cog(Thread_ReactRoles(bot))

"""

"adding reaction"
"fetch message id from initial message when thread is created"
"fetch emote:role from JSON"
"add reactions to message"

"deleting reaction"
"fetch message id from initial message when thread is created"
"clear all reactions from message"
"use 'adding reaction'"

"on reacting"
"fetch role associated with reaction"
"give role to thread recipient"

"on unreacting"
"fetch role associated with reaction"
"remove role from thread recipient"
"""
