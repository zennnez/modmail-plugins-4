import asyncio
import re

import discord
from discord.ext import commands
from discord.utils import get

from core import checks
from core.thread import Thread

class ImageSpoilers(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def sptr(self, ctx, *, message, anonymous, s_thread_recipient):
        #check if user is blocked
        if s_thread_recipient.id in self.bot.blocked_users:
            await ctx.message.add_reaction(self.config.blocked_emoji)
            return

        #if channel is DM channel
        if ctx.channel.guild is None:
            await ctx.message.add_reaction(self.config.sent_emoji)
            s_guild = discord.utils.get(self.bot.guilds, guild_id=self.config.modmail_guild_id) if self.config.modmail_guild_id is not None else discord.utils.get(self.bot.guilds, guild_id=self.config.guild_id)
            for channel in s_guild.channels:
                if re.search(f"{str(s_thread_recipient.id)}", channel.topic):
                    return await channel.send(content=f"(Response) Recipient: {message.content}", files=message.attachments)

        #if channel is thread channel
        else:
            s_dm_channel = discord.utils.get(self.bot.private_channels, recipient=s_thread_recipient)
            if anonymous is True:
                return await s_dm_channel.send(content=f"(Response) {ctx.author.top_role}: {message.content}", files=message.attachments)
            else:
                return await s_dm_channel.send(content=f"({ctx.author.top_role}) {str(ctx.author)}: {message.content}", files=message.attachments)


    @commands.Cog.listener()
    @checks.thread_only()
    async def on_thread_reply(self, thread, from_mod, message, anonymous, plain):
        s_thread_recipient = self.thread.recipient
        if message.author.bot:
            return

        #check if attachment is spoilered
        for attachment in message.attachments:
            if attachment.is_spoiler()
                return await sptr(message=message, anonymous-anonymous)
        
        #check if links are spoilered
        #links = re.findall("^(http:\/\/www\.|https:\/\/www\.|http:\/\/|https:\/\/)?[a-z0-9]+([\-\.]{1}[a-z0-9]+)*\.[a-z]{2,5}(:[0-9]{1,5})?(\/.*)?$", message.content)
        #for link in links:
        #if re.search("SPOILER_", link) is True:
        #return await sptr(message=message, anonymous-anonymous)

        #check if message contains "SPOILER_"
        if re.search("SPOILER_", message.content):
            return await sptr(message=message, anonymous=anonymous, s_thread_recipient=s_thread_recipient)
        
def setup(bot):
    bot.add_cog(ImageSpoilers(bot))