import asyncio

import discord
from discord.ext import commands

class Looper(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def loop(self, ctx, arg: bool, *, role: discord.Role):
        """
        To list members that have or don't have a specified role.
        0 list members without the role, while 1 lists members with the role.
        Command is case-sensitive.
        """
        x = 0
        if arg is False:
            for m in ctx.guild.members:
                if role in m.roles:
                    continue 
                else:
                    x += 1
                    await ctx.send(content=f"<@{m.id}>")
            return await ctx.send(content=f"Loop done! {x} members do not have {role.name}.")
        elif arg is True:
            for m in ctx.guild.members:
                if role not in m.roles:
                    continue 
                else:
                    x += 1
                    await ctx.send(content=f"<@{m.id}>")
            return await ctx.send(content=f"Loop done! {x} members have {role.name}.")
        else:
            return await ctx.send(content="Argument must be either True or False. Command is case-sensitive.")

def setup(bot):
    bot.add_cog(Looper(bot))
