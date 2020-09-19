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

def setup(bot):
    bot.add_cog(ReactRoles(bot))
