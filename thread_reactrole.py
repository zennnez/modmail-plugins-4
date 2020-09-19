import asyncio
import emoji
import re
import typing

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

class ReactRoles(commands.Cog):

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

    @commands.command(usage="[emoji] [role]")
    @checks.has.permissions(PermissionLevel.ADMINISTRATOR)
    async def threadreactrole_add(
        self,
        ctx,
        user: thread.recipient,
        emoji: Emoji,
        role: Union[discord.Role, str.lower]
    ):
        """
        Assigns a role to an emote for tickets.
        """
        emote = emoji.name if emoji.id is None else str(emoji.id)
        role_id = discord.Role.id

        role_dictionary = {emote: role_id}
        with open("thread_reactrole.json"


def setup(bot):
    bot.add_cog(ReactRoles(bot))

"""
"fetch emoji"
"fetch role"
"assign emoji to role"
"if there are open threads, use 'adding reaction'"
"finally, store emoji:role into JSON"

"adding reaction"
"fetch message id from initial message when thread is created"
"fetch emote:role from JSON"
"add reactions to message"

"delete command" "usage = reactrole remove [emoji] [optional: role]"
"find emoji from JSON"
"if there are open threads, use 'removing reaction'"
"finally, remove emoji:role from JSON"

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