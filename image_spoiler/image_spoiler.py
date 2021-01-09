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
    async def on_thread_reply(self, thread, from_mod, message, anonymous, plain):
        #check if attachment is spoilered
        for attachment in message.attachments:
            if attachment.filename.startswith("SPOILER_"):
                return await ctx.invoke(self.bot.get_command('pareply'), msg=message.content) if anonymous is True else await ctx.invoke(self.bot.get_command('preply'), msg=message.content)
        
        #check if links are spoilered
        #links = re.findall("^(http:\/\/www\.|https:\/\/www\.|http:\/\/|https:\/\/)?[a-z0-9]+([\-\.]{1}[a-z0-9]+)*\.[a-z]{2,5}(:[0-9]{1,5})?(\/.*)?$", message.content)
        #for link in links:
        #if re.search("SPOILER_", link) is True:
        #return await ctx.invoke(self.bot.get_command('pareply'), msg=message.content) if anonymous is True else await ctx.invoke(self.bot.get_command('preply'), msg=message.content)

        #check if message contains "SPOILER_"
        if re.search("SPOILER_", message.content):
            return await ctx.invoke(self.bot.get_command('pareply'), msg=message.content) if anonymous is True else await ctx.invoke(self.bot.get_command('preply'), msg=message.content)
        
def setup(bot):
    bot.add_cog(ImageSpoilers(bot))