import asyncio

import discord
from discord.ext import commands

class MessagePin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def pin(self, ctx, *, channel=discord.TextChannel):
        channel=channel
        PML = await channel.history(limit=1).flatten()
        PM = PML[0]
        return await PM.pin()

def setup(bot):
    bot.add_cog(MessagePin(bot))
