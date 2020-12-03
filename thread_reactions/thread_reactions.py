import asyncio
import typing
import emoji

import discord
from discord.ext import commands
from discord.role import Role

from core import checks
from core.models import PermissionLevel
from core.paginator import EmbedPaginatorSession
from core.utils import *

class UnicodeEmoji(commands.Converter):
    async def convert(self, ctx, argument):
        if argument in emoji.UNICODE_EMOJI:
            return discord.PartialEmoji(name=argument, animated=False)
        raise commands.BadArgument('Unknown emoji')

Emoji = typing.Union[discord.PartialEmoji, discord.Emoji, UnicodeEmoji]

class ThreadReactions(commands.Cog):
def __init__(self, bot):
    self.bot = bot
    
    @property
    def.thread_reactions(self) -> typing.Dict[str, int]:
        return self.config["thread_reactions"]
    
    @commands.group(aliases=["threadreactions", "threadreaction"], invoke_without_command=True)
    @checks.has_permissions(PermissionLevel.SUPPORTER)
    async def tr(self, ctx, *, name:Emoji)
        """
        help
        """
        
        if name is not None:
            val = self.bot.thread_reactions.get(name)
            if val is None:
                embed=create_not_found_embed(name, self.bot.thread_reactions.keys(), "Thread Reactions")
            else:
                embed = discord.Embed (
                    title=f"Thread Reactions - {name}:", description=get(guild.roles, id=val).name, color=self.bot.main_color
                )
            return await ctx.send(embed=embed)
        
        if not self.bot.thread_reactions:
            embed = discord.Embed (
                color=self.bot.error_color, description="You don\'t have any thread reactions at the moment."
            )
            embed.set_footer(text=f'Check "{self.bot.prefix}help tr add" to add a thread reaction.')
            embed.set_author(name="Thread Reactions", icon_url=ctx.guild.icon_url)
            return await ctx.send(embed=embed)
        
        embeds = []
        
        for i, names in enumerate(zip_longest(*(iter(sorted(self.bot.snippets)),) * 15)):
            description = format_description(i, names)
            embed = discord.Embed(color=self.bot.main_color, description=description)
            embed.set_author(name="Snippets", icon_url=ctx.guild.icon_url)
            embeds.append(embed)

        session = EmbedPaginatorSession(ctx, *embeds)
        await session.run()
        
    @tr.command(name="add")
    @checks.has_permissions(PermissionLevel.ADMINISTRATOR)
    async def tr_add(self, ctx, name:Emoji, *, value: discord.Role)
        """
        help
        """
        
        emote = name.name if name.id is None else str(name.id)
        
        if name in self.bot.thread_reactions:
            embed = discord.Embed(
                title="Error",
                color=self.bot.error_color,
                description=f"Thread reaction {name} already exists.",
            )
            return await ctx.send(embed=embed)
        
        if value not in self.guild.roles:
            embed = discord.Embed(
                title="Error",
                color=self.bot.error_color,
                description=f"Role not found.",
            )
            return await ctx.send(embed=embed)
        
        self.bot.thread_reactions[name] = value
        await self.bot.config.update()

        embed = discord.Embed(
            title="Added thread reaction",
            color=self.bot.main_color,
            description="Successfully created thread reaction.",
        )
        return await ctx.send(embed=embed)
    
    @tr.command(name="remove", aliases=["del", "delete"])
    @checks.has_permissions(PermissionLevel.ADMINISTRATOR)
    async def tr_remove(self, ctx, *, name:Emoji):
        """
        help
        """
        
        emote = name.name if name.id is None else str(name.id)
        
        if name in self.bot.thread_reactions:
            embed = discord.Embed(
                title="Removed thread reaction",
                color=self.bot.main_color,
                description=f"Thread reaction {name} is now deleted.",
            )
            self.bot.thread_reaction.pop(name)
            await self.bot.config.update()
        else:
            embed = create_not_found_embed(name, self.bot.thread_reactions.keys(), "Thread Reactions")
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(ThreadReactions(bot))
