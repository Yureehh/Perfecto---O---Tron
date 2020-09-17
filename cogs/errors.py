import discord
from discord.ext import commands

#Errors Handler class
#Still to be improved, inserted only most frequent errors at the moment
class ErrorsHandler(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    #Errors
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        # This prevents any commands with local handlers being handled here in on_command_error.
        if hasattr(ctx.command, 'on_error'):
            return

        if isinstance(error, commands.DisabledCommand):
            await ctx.send(f'{ctx.command} has been disabled.')

        elif isinstance(error, commands.MissingPermissions):
            await ctx.send(f"{ctx.author.name} is not allowed to use that command")

        elif isinstance(error, commands.MissingRequiredArgument ):
            await ctx.send("Please pass all required arguments")

        elif isinstance(error, commands.CommandNotFound):
            await ctx.send("Invalid command used, use .info to see all the commands")

        elif isinstance(error, commands.NoPrivateMessage):
            try:
                await ctx.author.send(f'{ctx.command} can not be used in Private Messages.')
            except discord.HTTPException:
                pass

def setup(bot):
    bot.add_cog(ErrorsHandler(bot))