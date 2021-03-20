import asyncio

import discord
from discord.ext import commands

class Looper(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def loop(self, ctx, *, role: discord.Role):
        for m in ctx.guild.members:
            for r in m.roles:
                if r is role:
                    break
            else:
                await ctx.send(content=f"<@{m.id}>")
        return await ctx.send(content="Loop done!")

def setup(bot):
    bot.add_cog(Looper(bot))