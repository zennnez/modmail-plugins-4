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

    @commands.Cog.listener()
    @checks.thread_only()
    async def on_thread_reply(self, thread, from_mod, message, anonymous, plain):
        if message.author.bot:
            return

        #convert attachments to files
        global s_file_list
        s_file_list = []
        for attachment in message.attachments if message.attachments is not None:
            file = await attachment.to_file()
            s_file_list.append(file)
            
        #check if attachment is spoilered
        for attachment in message.attachments:
            if attachment.is_spoiler():
                #check if user is blocked
                if thread.recipient.id in self.bot.blocked_users:
                    return await message.add_reaction(self.config.blocked_emoji)

                #if channel is DM channel
                if message.guild is None:
                    await message.add_reaction(self.config.sent_emoji)
                    s_guild = discord.utils.get(self.bot.guilds, guild_id=self.config.modmail_guild_id) if self.config.modmail_guild_id is not None else discord.utils.get(self.bot.guilds, guild_id=self.config.guild_id)
                    for channel in s_guild.channels:
                        if re.search(f"{str(thread.recipient.id)}", channel.topic):
                            return await channel.send(content=f"(Response) Recipient: {message.content}", files=s_file_list)

                #if channel is thread channel
                else:
                    s_dm_channel = discord.utils.get(self.bot.private_channels, recipient=thread.recipient)
                    if anonymous is True:
                        return await s_dm_channel.send(content=f"(Response) {message.author.top_role}: {message.content}", files=s_file_list)
                    else:
                        return await s_dm_channel.send(content=f"({message.author.top_role}) {str(message.author)}: {message.content}", files=s_file_list)

        
        #check if links are spoilered
        #links = re.findall("^(http:\/\/www\.|https:\/\/www\.|http:\/\/|https:\/\/)?[a-z0-9]+([\-\.]{1}[a-z0-9]+)*\.[a-z]{2,5}(:[0-9]{1,5})?(\/.*)?$", message.content)
        #for link in links:
        #if re.search("SPOILER_", link) is True:
        #return await sptr(message=message, anonymous-anonymous)

        #check if message contains "SPOILER_"
        if re.search("SPOILER_", message.content):
            #check if user is blocked
            if thread.recipient.id in self.bot.blocked_users:
                return await message.add_reaction(self.config.blocked_emoji)

            #if channel is DM channel
            if message.guild is None:
                await message.add_reaction(self.config.sent_emoji)
                s_guild = discord.utils.get(self.bot.guilds, guild_id=self.config.modmail_guild_id) if self.config.modmail_guild_id is not None else discord.utils.get(self.bot.guilds, guild_id=self.config.guild_id)
                for channel in s_guild.channels:
                    if re.search(f"{str(thread.recipient.id)}", channel.topic):
                        return await channel.send(content=f"(Response) Recipient: {message.content}", files=s_file_list)

            #if channel is thread channel
            else:
                s_dm_channel = discord.utils.get(self.bot.private_channels, recipient=thread.recipient)
                if anonymous is True:
                    return await s_dm_channel.send(content=f"(Response) {message.author.top_role}: {message.content}", files=s_file_list)
                else:
                    return await s_dm_channel.send(content=f"({message.author.top_role}) {str(message.author)}: {message.content}", files=s_file_list)
        
def setup(bot):
    bot.add_cog(ImageSpoilers(bot))