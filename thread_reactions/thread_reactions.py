import asyncio
import emoji
import typing

import discord
from discord.ext import commands
from discord.utils import get

from core import checks
from core.models import PermissionLevel
from core.config import *
from core.utils import *
from core.thread import Thread

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

        To add reactions to thread, do: '{prefix}thr add'
        """

        if not thread_reactions:
            embed=discord.Embed(
                color=self.bot.error_color,
                description="You dont have any thread reaction roles at the moment"
            )
            embed.set_footer(text=f"Check'{self.bot.prefix}help tr add' to add a reaction role.")
            return await ctx.send(embed=embed)

        global tr_embeds
        tr_embeds = discord.Embed(
            title="Thread Reactions",
            color=self.bot.main_color
        )

        for key in thread_reactions:
            Emote = discord.utils.get(ctx.bot.emojis, id=int(key)) if key.isdigit() is True else emoji.emojize(key)
            Role = self.bot.guild.get_role(int(thread_reactions[key]))
            EmoteName = str(Emote)
            RoleName = str(Role)
            tr_embeds.add_field(name=EmoteName, value=RoleName)
            continue

        return await ctx.send(embed=tr_embeds)

    @tr.command(name="add")
    @checks.has_permissions(PermissionLevel.ADMINISTRATOR)
    async def tr_add(self, ctx, name:EmojiOBJ, *, value:discord.Role):
        """
        Add a reaction role.

        To add a reaction, do: '{prefix}tr add emoji role'
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

        To remove a reaction, do: '{prefix}tr remove emoji'
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

    @commands.group(invoke_without_command=True)
    @checks.has_permissions(PermissionLevel.SUPPORTER)
    @checks.thread_only()
    async def thr(self, ctx):
        """
        Edits reactions on thread genesis message.

        To update reactions, do: '{prefix}trt update'
        """
        return await ctx.send_help(ctx.command)

    @thr.command(name="update")
    @checks.has_permissions(PermissionLevel.ADMINISTRATOR)
    @checks.thread_only()
    async def thr_update(self, ctx):
        """
        Updates reactions on thread genesis message.
        """

        msg = await ctx.channel.history(limit=1, oldest_first=True).flatten()
        msg = msg[0]

        await msg.clear_reactions()
        for key in thread_reactions:
            if key.isdigit() is True:
                Emote = discord.utils.get(ctx.bot.emojis, id=int(key))
                await msg.add_reaction(Emote)
                continue
            else:
                await msg.add_reaction(key)
                continue
        
        embed=discord.Embed(
            color=self.bot.main_color,
            description="Reactions updated."
        )
        return await ctx.send(embed=embed)

    @commands.Cog.listener()
    @checks.thread_only()
    async def on_thread_ready(self, thread):
        msg = thread.genesis_message
        for key in thread_reactions:
            if key.isdigit() is True:
                Emote = discord.utils.get(self.bot.emojis, id=int(key))
                await msg.add_reaction(Emote)
                continue
            else:
                await msg.add_reaction(key)
                continue
        return

    @commands.Cog.listener()
    @checks.thread_only()
    async def on_raw_reaction_add(self, payload):

        Emote = payload.emoji.name if payload.emoji.id is None else str(payload.emoji.id)
        Guild = self.bot.get_guild(payload.guild_id)
        Channel = Guild.get_channel(payload.channel_id)
        ChannelT = Channel.topic
        recipientID = [int(word) for word in ChannelT.split() if word.isdigit()]
        recipientID = recipientID[0]
        recipientOBJ = Guild.get_member(recipientID)

        if Emote in thread_reactions:
            RoleID = int(thread_reactions[Emote])
            RoleOBJ = Guild.get_role(RoleID)
            await recipientOBJ.add_roles(roleOBJ)
            embed = discord.Embed(
                color=self.bot.main_color,
                description=f"Successfully added {str(RoleOBJ)} from {str(recipientOBJ)}."
            )
            return await Channel.send(embed=embed)        

    @commands.Cog.listener()
    @checks.thread_only()
    async def on_raw_reaction_remove(self, payload):

        Emote = payload.emoji.name if payload.emoji.id is None else str(payload.emoji.id)
        Guild = self.bot.get_guild(payload.guild_id)
        Channel = Guild.get_channel(payload.channel_id)
        ChannelT = Channel.topic
        recipientID = [int(word) for word in ChannelT.split() if word.isdigit()]
        recipientID = recipientID[0]
        recipientOBJ = Guild.get_member(recipientID)

        if Emote in thread_reactions:
            RoleID = int(thread_reactions[Emote])
            RoleOBJ = Guild.get_role(RoleID)
            await recipientOBJ.remove_roles(roleOBJ)
            embed = discord.Embed(
                color=self.bot.main_color,
                description=f"Successfully removed {str(RoleOBJ)} from {str(recipientOBJ)}."
            )
            return await Channel.send(embed=embed)        

def setup(bot):
    bot.add_cog(ThreadReactions(bot))