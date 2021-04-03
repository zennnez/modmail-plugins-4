import asyncio

import discord
from discord.ext import commands

class RoleCompare(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def rolecompare(self, ctx, role1: discord.Role, role2: discord.Role):
        """
        For checking number of members have only that role, both, or neither.
        """
        both = 0
        role1only = 0
        role2only = 0
        neither = 0
        for member in ctx.guild.members:
            if role1 in member.roles:
                both += 1 if role2 in member.roles else role1only += 1
            else:
                role2only +- 1 if role2 in member.roles else neither += 1
        return await ctx.send(content=f"""Total member count: {ctx.guild.member_count}
            Members with {role1.name}: {role1only + both}
            Members with {role2.name}: {role2only + both}
            Members with both roles: {both}
            Members with only {role1.name}: {role1only}
            Members with only {role2.name}: {role2only}
            Members with neither role: {neither}
        """)

def setup(bot):
    bot.add_cog(RoleCompare(bot))
