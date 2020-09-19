import asyncio
import emoji
import re
import typing
import json

import discord
from discord.ext import commands

from core import checks
from core.models import PermissionLevel

class UnicodeEmoji(commands.Converter):
    async def convert(self, ctx, argument):
        if argument in emoji.UNICODE_EMOJI:
            return discord.PartialEmoji(name=argument, animated=False)
        raise commands.BadArgument('Unknown emoji')

Emoji = typing.Union[discord.PartialEmoji, discord.Emoji, UnicodeEmoji]
role_dictionary = {}

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
    
    @commands.command(name="add", usage="[emoji] [role]")
    @checks.has.permissions(PermissionLevel.ADMINISTRATOR)
    async def threadreactrole_add(
        self,
        ctx,
        *
        emoji: Emoji,
        role: Union[discord.Role, str.lower]
    ):
        """
        Assigns a role to an emote for tickets.
        """
        emote = emoji.name if emoji.id is None else str(emoji.id)
        role_id = discord.Role.id

        role_dictionary = {emote: role_id}
        with open("thread_reactrole.json", "r+") as file:
            data=json.load(file)
            data.update(role_dictionary)
            file.seek(0)
            json.dump(data, file)
    
    @commands.command(name="remove", usage="[emoji]")
    @checks.has.permissions(PermissionLevel.ADMINISTRATOR)
    async def threadreactrole_remove(
        self,
        ctx,
        *
        emoji: Emoji
    ):
        """
        Removes the role from the emote for tickets.
        """

        emote = emoji.name if emoji.id is None else str(emoji.id)
        with open("thread_reactrole.json", "r+") as file:
            data=json.load(file)
            data.pop(emote, not_found=None)
            file.seek(0)
            json.dump(data, file)

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