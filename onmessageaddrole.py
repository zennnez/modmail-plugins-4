from discord.ext import commands

class OnMessageAddRole(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(name="onmessageaddrole", aliases="omar", invoke_without_command=True)
    @checks.has_permissions(PermissionLevel.MODERATOR)
    async def onmessageaddrole(self, ctx, role: discord.Role, ):
        """Assign roles to members when they type in specified channel."""
        channelroles = []
        
        @omar.command(name="add")
        @checks.has_permissions(PermissionLevel.MODERATOR)
        async def omar_add(self, ctx, *, role: discord.Role, channel:discord.TextChannel.id):
            channelroles[channel]=role

        @commands.Cog.listener()
        async def on_message(self, member):
            member = context.author
            for channel in channelroles:
                role = channelroles.get(channel)
                if role in member.roles:
                    continue
                else:
                    member.add_role(role)


def setup(bot):
    bot.add_cog(OnMessageAddRole(bot))