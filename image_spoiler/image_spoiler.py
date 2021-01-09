import asyncio
import re

import discord
from discord.ext import commands

from core import checks
from core.thread import Thread

class ImageSpoilers(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    @checks.thread_only()
    async def on_message(self, ctx):
        msg = ctx.message
        global lic
        lic = 0
        if not ctx.author.bot:
            for attachment in msg.attachments:
                if attachment.filename.startswith("SPOILER_"):
                    lic += 1
            links = re.findall(r"[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)", msg.content)
            for key in links:
                spoiler = re.search("SPOILER_",str(key))
                if spoiler is not None:
                    lic += 1
        
        if lic > 0:
            return await ctx.thread.reply(msg, plain=True)

                

def setup(bot):
    bot.add_cog(ImageSpoilers(bot))