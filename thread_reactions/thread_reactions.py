import asyncio
import typing
from itertools import takewhile, zip_longest

import discord
from discord.ext import commands
from discord.utils import get

from core import checks
from core.models import PermissionLevel
from core.paginator import EmbedPaginatorSession
from core.utils import *
from core.thread import Thread

class UnicodeEmoji(commands.Converter):
    async def convert(self, ctx, argument):
        if argument in emoji.UNICODE_EMOJI:
            return discord.PartialEmoji(name=argument, animated=False)
        raise commands.BadArgument('Unknown emoji')
    
emojiObj = typing.Union[discord.PartialEmoji, discord.Emoji, UnicodeEmoji]



class ThreadReactions(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @property
    def thread_reactions(self) -> typing.Dict[str, str]:
        return self.config["thread_reactions"]

    def tr_format_descriptiom(i, name, value):
        return "\n".join(
            ": ".join((str(a + i * 15), b, c))
            for a, b, c in enumerate(takewhile(lambda x: x is not None, names, values), start=1)
        )

    @commands.group(aliases=["threadreactions", "threadreaction"], invoke_without_command=True)
    @checks.has_permissions(PermissionLevel.SUPPORTER)
    async def tr(self, ctx):
        """
        Creates reactions to thread genesis message for assigning roles.

        When '{prefix}tr' is used by itself, this will retrieve
        a list of reaction roles currently assigned.

        To add reactions to thread:
        - '{prefix}trt add emoji|role(optional)'
        """

        if not self.bot.thread_reactions:
            embed = discord.Embed(
                color=self.bot.error_color, description="You dont have any reaction roles at the moment."
            )
            embed.set_footer(text=f'Check "{self.bot.prefix}help tr add" to add a reaction role.')
            embed.set_author(name="Thread Reactions", icon_url=ctx.guild.icon_url)
            return await ctx.send(embed=embed)

        embeds = []

        for i, names, values in enumerate(zip_longest(*(iter(sorted(self.bot.thread_reactions)),) * 15)):
            description = tr_format_description(i, names, values)
            embed = discord.Embed(color=self.bot.main_color, description=description)
            embed.set_author(name="Thread Reactions", icon_url=ctx.guild.icon_url)
            embeds.append(embed)

        session = EmbedPaginatorSession(ctx, *embeds)
        await session.run()

    @tr.command(name="add")
    @checks.has_permissions(PermissionLevel.ADMINISTRATOR)
    async def tr_add(self, ctx, name: emojiObj, *, value: discord.Role):
        """
        Add a reaction role.

        To add a reaction, do: '''
        {prefix}tr add emoji role
        '''
        """

        emote = name.name if name.id is None else str(name.id)
        role = str(value.id)
        Name = str(name)
        Value = value.name
        if name in self.bot.thread_reactions:
            if value is self.bot.thread_reactions[name]:
                embed = discord.Embed(
                    title="Error",
                    color=self.bot.error_color,
                    description=f"{Value} is already assigned to {Name}"
                )
                return await ctx.send(embed=embed)
            else:
                embed = discord.Embed(
                    color=self.bot.main_color,
                    description=f"{Name} is currently assigned to {self.bot.thread_reactions[name]}. Will you like to replace it with {Value}?"
                )
                msg = await ctx.send(embed=embed)
                await msg.add_reaction(self.bot.confirm_thread_creation_accept)
                await msg.add_reaction(self.bot.confirm_thread_creation_deny)

                await msg.on_raw_reaction_add(payload)
                if payload.emoji is self.bot.confirm_thread_creation_accept:
                    await msg.clear_reactions()
                    await self.bot.thread_reactions.update({emote:role})
                    embed = discord.Embed(
                        title="Reaction role updated",
                        color=self.bot.main_color,
                        description=f"{Name} has now been assigned to {Value}"
                    )
                    return await ctx.send(embed=embed)
                else if payload.emoji is self.bot.confirm_thread_creation_deny:
                    await msg.clear_reactions()
                    embed = discord.Embed(
                        title="Denied",
                        color-=self.bot.error_color,
                        description="Permission denied"
                    )
                    return await ctx.send(embed=embed)
                await asyncio.sleep(60)
                await msg.clear_reactions()
                return

        for Emote, Role in self.bot.thread_reactions():
            if Role == role:
                embed = discord.Emned(
                    color=self.bot.main_color,
                    description=f"{Value} is currently assigned with {str(Emote)}. Will you like to replace it with {Name}?"
                )
                msg = await ctx.send(embed=embed)
                await msg.add_reaction(self.bot.confirm_thread_creation_accept)
                await msg.add_reaction(self.bot.confirm_thread_creation_deny)
                await msg.on_raw_reaction_add(payload):
                if payload.emoji is se;f.bot.confirm_thread_creation_accept:
                    await msg.clear_reactions()
                    await self.bot.thread_Reactions.pop(Emote)
                    await self.bot.thread_reactions.update({emote:role})
                    embed = discord.Embed(
                        title="Reaction role updated",
                        color=self.bot.main_color,
                        description=f"{Value} has now been assigned to {Name}"
                    )
                    return await ctx.send(embed=embed)
                else if payload.emoji is self.bot.confirm_thread_creation_deny:
                    await msg.clear_reactions()
                    embed = discord.Embed(
                        title="Denied",
                        color-=self.bot.error_color,
                        description="Permission denied"
                    )
                    return await ctx.send(embed=embed)
                await asyncio.sleep(60)
                await msg.clear_reactions()
                return

        self.bot.thread_reactions[name] = value

        embed = discord.Embed(
            title="Reaction role added",
            color=self.bot.main_color,
            description=f"{Name} has been assigned to {Value}"
        )
        return await ctx.send(embed=embed)

    @tr.command(name="remove", aliases=["del", "delete"])
    @checks.has_permissions(PermissionLevel.ADMINISTRATOR)
    async def tr_remove(self, ctx, *, name=emojiObj or discord.Role)
        """
        Remove a reaction role.

        To remove a reaction role, do: '''
        {prefix}tr remove emoji|role
        '''
        """

        Name = str(name)
        emote = name.name if name.id is None else str(name.id)
        role = name.id
        if type(name) is emojiObj:
            if name not in self.bot.thread_reactions:
                embed = discord.Embed(
                    title="Error",
                    color=self.bot.error_color,
                    description=f"{Name} is unassigned."
                )
            else:
                self.bot.thread_reactions.pop(emote)
                embed = discord.Embed(
                    title="Reaction role removed",
                    color=self.bot.main_color,
                    description=f"{Name} has been unassigned from {self.bot.thread_reactions[emote]}."
                )
        else if type(name) is discord.Role:
            for Emote, Role in self.bot.thread_reactions:
                if Role == role:
                    self.bot.thread_reactions.pop(Emote)
                    embed = discord.Embed(
                        title="Reaction role removed",
                        color=self.bot.main_color,
                        description=f"{Name} has been unassigned from {str(Emote)}."
                    )
            embed= discord.Embed(
                title="Error",
                color=self.bot.error_color,
                description=f"{Name} is unassigned."
            )
        return await ctx.send(embed=embed)

    @commands.group(aliases=["threadreactionsthread", "threadreactionthread"], invoke_without_command=True)
    @checks.has_permissions(PermissionLevel.ADMINISTRATOR)
    @checks.thread_only()
    async def trt(self, ctx):
        """
        Edits reactions on thread genesis message.

        To update reactions, do: '''
        {prefix}trt update
        '''
        """
        return await ctx.send_help(ctx.command)

    @trt.command(name="update")
    @checks.has_permissions(PermissionLevel.ADMINISTRATOR)
    @checks.thread_only()
    async def trt_update(self, ctx):
        """
        Updates reactions on thread genesis message.
        """

        async for message in ctx.channel.history(limit=1, oldest_first=True):
            await message.clear_reactions()
            for Emote, Role in self.bot.thread_reactions:
                if Emote.isdigit() is True:
                    EmoteID = int(Emote)
                    EmoteOBJ = discord.utils.get(bot.get_all_emoji(), id=EmojiID)
                    await message.add_reaction(EmoteOBJ)
                else:
                    EmoteOBJ = discord.utils.get(bot.get_all_enoji(), name=Emote)
                    await message.add_reaction(EmoteOBJ)

            embed=discord.Embed(
                title="Reactions updated",
                color=self.bot.main_color,
                description="Thread reactions have been updated."
            )
            return await ctx.send(embed=embed)
            
    @trt.command(name="add")
    @checks.has_permissions(PermissionLevel.ADMINISTRATOR)
    @checks.thread_only()
    async def trt_add(self, ctx):
        """
        Adds reactions to thread genesis message.
        
        For updating existing reactions, do: '''
        {prefix}trt update
        '''
        """

        async for message in ctx.channel.history(limit=1, oldest_first=True):
            if message.reactions is not None:
                embed=discord.Embed(
                    title='Error',
                    color=self.bot.error_color,
                    description=f"Reactions already present. Use '{prefix}trt update' to update reactions."
                )
                return await ctx.send(embed=embed)

            for Emote, Role in self.bot.thread_reactions:
                if Emote.isdigit() is True:
                    EmoteID = int(Emote)
                    EmoteOBJ = discord.utils.get(bot.get_all_emoji(), id=EmojiID)
                    await message.add_reaction(EmoteOBJ)
                else:
                    EmoteOBJ = discord.utils.get(bot.get_all_enoji(), name=Emote)
                    await message.add_reaction(EmoteOBJ)

            embed=discord.Embed(
                title="Reactions added",
                color=self.bot.main_color,
                description="Thread reactions have been added."
            )
            return await ctx.send(embed=embed)

    @trt.command(name="remove", aliases=["del", "delete"])
    @checks.has_permissions(PermissionLevel.ADMINISTRATOR)
    @checks.thread_only()
    async def trt_remove(self, ctx):
        """
        Removes reactions from thread genesis message.

        For adding reactions, do either
        '''
        {prefix}trt add
        '''
        or
        '''
        {prefix}trt update
        '''
        """

        async for message in ctx.channel.history(limit=1, oldest_first=True):
            if message.reactions is None:
                embed=discord.Embed(
                    title='Error',
                    color=self.bot.error_color,
                    descriptio=f"No reactions present. Use '{prefix}trt add' to add reactions."
                )
                return await ctx.send(embed=embed)

            await message.clear_reactions()
            embed-discord.Embed(
                title="Reactions removed",
                color=self.bot.main_color,
                description="Thread reactions have been removed."
            )
            return await ctx.send(embed=embed)
    
    @commands.Cog.listener()
    async def on_thread_ready(self, thread):
        for Emote, Role in self.bot.thread_reactions:
            if Emote.isdigit() is True:
                EmoteID = int(Emote)
                EmoteOBJ = discord.utils.get(bot.get_all_emoji(), id=EmojiID)
                await thread.genesis_message.add_reaction(EmoteOBJ)
            else:
                EmoteOBJ = discord.utils.get(bot.get_all_enoji(), name=Emote)
                await thread.genesis_message.add_reaction(EmoteOBJ)
        return

    @commands.Cog.listener()
    @checks.thread_only()
    async def on_raw_reaction_add(self, ctx, thread, payload):
        if payload.message_id is not thread.genesis_message.id:
            return
        
        emojiReaction = payload.emoji.name if payload.emoji.id is None else str(payload.emoji.id)

        if emojiReaction in self.bot.thread_reactions:
            roleOBJ = self.guild.get_role(int(self.bot.thread_reactions[emojiReaction]))
            if roleOBJ.position > payload.member.top_role.position:
                await thread,genesis_message.remove(payload.memeber)
                embed=discord.Embed(
                    color=self.bot.error_color,
                    description="You lacked permissions to grant the role."
                )
                return await ctx.send(embed=embed)
            
            await thread.recipent.add_roles(roleOBJ)
            embed = discord.Embed(
                title="Role successfully added",
                color=self.bot.main_color,
                description=f"{roleOBJ.name} has been successfully granted to {thread.recipent.name}."
            )
            return await ctx.send(embed=embed)
        return

    @commands.Cog.listener()
    @checks.thread_only()
    async def on_raw_reaction_remove(self, ctx, thread, payload):
        if payload.message_id is not thread.genesis_message.id:
            return

        emojiReaction = payload.emoji.name if payload.emoji.id is None else str(payload.emoji.id)
        memberOBJ = self.guild.get_member(payload.user_id)

        if emojiReaction in self.bot.thread_reactions:
            roleOBJ = self.guild.get_role(int(self.bot.thread_reactions[emojiReaction]))
            await thread.recipent.remove_roles(roleOBJ)
            embed = discord.Embed(
                title="Role successfully removed",
                color=self.bot.main_color,
                description=f"{roleOBJ.name} has been successfully removed from {thread.recipent.name}."
            )
            return await ctx.send(embed=embed)
        return

def setup(bot):
    bot.add_cog(ThreadReactions(bot))