"import whatever is needed"
import asyncio
import emoji

import discord
from discord.ext import commands

from core import checks
from core.models import PermissionLevel
"set up emotes"

"master command"
class ReactRoles(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.db = bot.plugin_db.get_partition(self)
        
commands.group(name="reactrole" invoke_without_command=True)
@checks.has_permissions(PermissionLevel.ADMINISTRATOR)
async def reactrole(self, ctx: commands.Context):
    "Creates tickets with reactions, allowing users to assign roles to ticket recipients."
    await ctx.send_help(ctx.command)

"add command" "usage = reactrole add [emoji] [role]"
"fetch emoji"
"fetch role"
"assign emoji to role"
"if there are open threads, use 'adding reaction'"
"finally, store emoji:role into JSON"

"adding reaction"
"fetch message id from initial message when thread is created"
"fetch emote:role from JSON"
"add reactions to message"

"delete command" "usage = reactrole remove [emoji] [optional: role]"
"find emoji from JSON"
"if there are open threads, use 'removing reaction'"
"finally, remove emoji:role from JSON"

"deleting reaction"
"fetch message id from initial message when thread is created"
"clear all reactions from message"
"use 'adding reaction'"

"on reacting"
"fetch role associated with reaction"
"give role to thread recipient"

"on unreacting"
"fetch role associated with reaction"
"remove role from thread recipient"

"setup bot and add cog to plugin"
def setup(bot):
    bot.add_cog(ReactRoles(bot))
