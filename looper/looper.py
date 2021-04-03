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
        False list members without the role, while True lists members with the role.
        Command is case-sensitive.
        """
        if arg is False:
            for m in ctx.members:
                if role in m.roles:
                    continue 
                else:
                    await ctx.send(content=f"<@{m.id}>")
            return await ctx.send(content="Loop done!")
        elif arg is True:
            for m in ctx.members:
                if role not in m.roles:
                    continue 
                else:
                    await ctx.send(content=f"<@{m.id}>")
            return await ctx.send(content="Loop done!")
            return await ctx.send(content="Loop done!")
        else:
            return await ctx.send(content="Argument must be either True or False, case-sensitive.")

def setup(bot):
    bot.add_cog(Looper(bot))
