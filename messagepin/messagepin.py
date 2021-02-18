import asyncio

import discord
from discord.ext import commands
from discord.utils import get

class MessagePin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def pin(self, ctx, *, channel):
        CHN = discord.utils.get(ctx.guild.text_channels, id=int(channel))
        PML = await CHN.history(limit=1).flatten()
        PM = PML[0]
        await PM.pin()
        return await ctx.send(content="Done!")

def setup(bot):
    bot.add_cog(MessagePin(bot))
