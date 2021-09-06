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
"""
class EmojiCO(commands.PartialEmojiConverter):
    async def convert(self, ctx, argument):
        if argument in emoji.UNICODE_EMOJI:
            return discord.PartialEmoji(name=emoji.demojize(argument), animated=False)
        raise commands.BadArgument("Unknown emoji")

EmojiOBJ = typing.Union[discord.PartialEmoji, discord.Emoji, EmojiCO]
"""     

EmojiOBJ= typing.Union[discord.PartialEmoji, discord.Emoji, str]       

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

        def emojiCheck(arg):
            if type(arg) == str:
                arg = emoji.demojize(arg) if arg in UNICODE_EMOJI["en"] else None
            else:
                arg = arg.name if arg.id is None else str(arg.id)
            return arg

        if not emojiCheck(name):
            embed = discord.Embed(
                color=self.bot.error_color,
                description="Invalid emoji provided"
            )
            return await ctx.send(embed=embed)

        emote = emojiCheck(name)
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

        def emojiCheck(arg):
            if type(arg) == str:
                arg = emoji.demojize(arg) if arg in UNICODE_EMOJI["en"] else None
            else:
                arg = arg.name if arg.id is None else str(arg.id)
            return arg

        if not emojiCheck(name):
            embed = discord.Embed(
                color=self.bot.error_color,
                description="Invalid emoji provided"
            )
            return await ctx.send(embed=embed)

        emote = emojiCheck(name)

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
    
        if payload.guild_id is None:
            return
        
            Emote = payload.emoji.name if payload.emoji.id is None else str(payload.emoji.id)
            Channel = self.bot.modmail_guild.get_channel(payload.channel_id)
            User = self.bot.guild.get_member(payload.user_id)
            Thread = await self.bot.threads.find(channel=Channel)
        
            if User.bot:
                return   
            elif Thread is None:
                return
            elif Emote not in thread_reactions:
                return
            
            RoleID = int(thread_reactions[Emote])
            RoleOBJ= self.bot.guild.get_role(RoleID)
        
            if len(Thread.recipients) == 1:
                RecipientOBJ = Thread.recipients[0]
                await RecipientOBJ.add_roles(RoleOBJ)
                embed = discord.Embed(
                    color=self.bot.main_color,
                    description=f"Successfully added {str(RoleOBJ)} to {str(RecipientOBJ)}."
                )
                return await Channel.send(embed=embed)
        
            global recipientEmbed
            recipientEmbed = discord.Embed(
                title=f"Recipient Selection for adding {str(RoleOBJ)}",
                color=self.bot.main_color,
            )
        
            global rE_index
            rE_index = 0
        
            for recipient in Thread.recipients:
                recipientEmbed.add_field(value=f"{str(rE_index + 1)} - {str(recipient)}")
                rE_index = rE_index + 1
                continue
            
            await Channel.send(embed=recipientEmbed)
            
            def check(m):
                return m.content.isdigit() and int(m.content) <= rE_index + 1
                
            reply = await client.wait_for("message", check=check, timeout=60)
            RecipientOBJ = Thread.recipients[int(reply)-1]
            await RecipientOBJ.add_roles(RoleOBJ)
            embed = discord.Embed(
                color=self.bot.main_color,
                description=f"Successfully added {str(RoleOBJ)} to {str(RecipientOBJ)}."
            )
            return await Channel.send(embed=embed)       

    @commands.Cog.listener()
    @checks.thread_only()
    async def on_raw_reaction_remove(self, payload):
    
        if payload.guild_id is None:
            return
        
            Emote = payload.emoji.name if payload.emoji.id is None else str(payload.emoji.id)
            Channel = self.bot.modmail_guild.get_channel(payload.channel_id)
            User = self.bot.guild.get_member(payload.user_id)
            Thread = await self.bot.threads.find(channel=Channel)
        
            if User.bot:
                return   
            elif Thread is None:
                return
            elif Emote not in thread_reactions:
                return
            
            RoleID = int(thread_reactions[Emote])
            RoleOBJ= self.bot.guild.get_role(RoleID)
        
            if len(Thread.recipients) == 1:
                RecipientOBJ = Thread.recipients[0]
                await RecipientOBJ.remove_roles(RoleOBJ)
                embed = discord.Embed(
                    color=self.bot.main_color,
                    description=f"Successfully removed {str(RoleOBJ)} to {str(RecipientOBJ)}."
                )
                return await Channel.send(embed=embed)
        
            global recipientEmbed
            recipientEmbed = discord.Embed(
                title=f"Recipient Selection for removing {str(RoleOBJ)}",
                color=self.bot.main_color,
            )
        
            global rE_index
            rE_index = 0
        
            for recipient in Thread.recipients:
                recipientEmbed.add_field(value=f"{str(rE_index + 1)} - {str(recipient)}")
                rE_index = rE_index + 1
                continue
            
            await Channel.send(embed=recipientEmbed)
            
            def check(m):
                return m.content.isdigit() and int(m.content) <= rE_index + 1
                
            reply = await client.wait_for("message", check=check, timeout=60)
            RecipientOBJ = Thread.recipients[int(reply)-1]
            await RecipientOBJ.remove_roles(RoleOBJ)
            embed = discord.Embed(
                color=self.bot.main_color,
                description=f"Successfully removedd {str(RoleOBJ)} to {str(RecipientOBJ)}."
            )
            return await Channel.send(embed=embed)          

def setup(bot):
    bot.add_cog(ThreadReactions(bot))