import discord
from discord.ext import commands

class Admin(commands.Cog):

    def __init__(self, bot):
        self.bot = bot


    @commands.command(name = "clear", aliases=["clearMessages", "clearChat", "Clear"], help = """The command clears the last X messages int he discord chat, where X is passed as an argument.
                                                                                                It deletes also the command call itself so has to be counted 1 more than the actual amount""" )
    @commands.has_permissions(manage_messages = True)
    async def clear_messages(self, ctx, amount = 2):
        await ctx.channel.purge(limit = amount)

    @commands.command(name = "disconnect", aliases = ["Disc", "disc", "disconnectUser"], help = "disconnects a user if the caller has the permissions")
    @commands.has_permissions(kick_members = True)
    async def disconnectUser(self, ctx, member : discord.Member, *, reason = None):
        await discord.Member.disconnect()

    #the asterisc takes all the parameters passed after the command and puts it into reason, to cover usernames with spaces
    @commands.command(name = "kick",aliases = ["kickUser", "Kick"], ,  help = "kicks a user if the caller has the permissions")
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member : discord.Member, *, reason = None):
        await member.kick(reason = reason)

    #bans a user
    @commands.command(name = "ban",aliases = ["banUser", "Ban"], help = "bans a user if the caller has the permissions")
    @commands.has_permissions(ban_members=True)
    async def ban_user(self, ctx, member : discord.Member, *, reason = None):
        await member.ban(reason = reason)

    #unban a user
    @commands.command(name = "unban", aliases = ["sban", "unbanUser", "Unban"], help = "unbans a user")
    @commands.has_permissions(ban_members=True)
    async def unbanUser(self, ctx, *, member):
        bannedUsers = await ctx.guild.bans()
        memberName, memberDiscriminator = member.split("#")

        for banned in bannedUsers:
            user = banned.user

            if (user.name, user.discriminator) == (memberName, memberDiscriminator):
                await ctx.guild.unban(user)
                await ctx.send(f"Unbanned {user.mention}")
                return

def setup(bot):
    bot.add_cog(Admin(bot))