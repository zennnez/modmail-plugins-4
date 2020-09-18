import asyncio
import emoji
import re
import typing

import discord
from discord.ext import commands

from core import checks
from core.models import PermissionLevel
from core.thread import thread

class UnicodeEmoji(commands.Converter):
    async def convert(self, ctx, argument):
        if argument in emoji.UNICODE_EMOJI:
            return discord.PartialEmoji(name=argument, animated=False)
        raise commands.BadArgument('Unknown emoji')

Emoji = typing.Union[discord.PartialEmoji, discord.Emoji, UnicodeEmoji]

@commands.group(aliases=["reactrole"], invoke_without_command=True,)
    @checks.has_permissions(PermissionLevel.ADMINISTRATOR)
    async def reactrole(self, ctx: commands.Context):
        """
        When thread is created, reactions are added.
        These reactions can be used to assign oles to users.
        """

    @snippet.command(name="add")
    @checks.has_permissions(PermissionLevel.ADMINISTRATOR)
    async def reactrole_add(self, ctx, user: Optional[User] = None, *, role: discord.Role, emoji: Emoji,):
        """
        Adds reaction to beginning of future threads.
        """
        user = thread.recipient

        emote = emoji.name if emoji.id is None else str(emoji.id)
        msg= await thread.send(message)

        await self.db.find_one_and_update(
            {"_id": "config"}, {"$set": {emote: {"role": role.id, "state": "unlocked"}}},
            upsert=True)
        await self.bot.add_reaction(msg, emoji)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, User=None, payload):
        if not payload.guild_id:
            return
        
        config = await self.db.find_one({"_id": "config"})
        
        emote = payload.emoji.name if payload.emoji.id is None else str(payload.emoji.id)
        emoji = payload.emoji.name if payload.emoji.id is None else payload.emoji
        
        guild = self.bot.get_guild(payload.guild_id)
        member = discord.utils.get(guild.members, id=payload.user_id)
        
        if member.bot:
            return
        
        try:
            msg_id = config[emote]["msg_id"]
        except (KeyError, TypeError):
            return
        
        if payload.message_id != int(msg_id):
            return
        
        ignored_roles = config[emote].get("ignored_roles")
        if ignored_roles:
            for role_id in ignored_roles:
                role = discord.utils.get(guild.roles, id=role_id)
                if role in member.roles:
                    await self._remove_reaction(payload, emoji, member)
                    return
        
        state = config[emote].get("state", "unlocked")
        if state and state == "locked":
            await self._remove_reaction(payload, emoji, member)
            return
        
        rrole = config[emote]["role"]
        role = discord.utils.get(guild.roles, id=int(role))

        if role:
            await member.add_roles(role)


def setup(bot):
    bot.add_cog(ThreadReactRole(bot))