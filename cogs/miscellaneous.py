import discord
from discord.ext import commands
from random import choice

class Start(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        n = after.nick
        if n:
            if n.lower().count("Yureeh") > 0:
                await after.edit(nick = "Te piacess")




    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f"Your ping is {round(self.bot.latency * 1000)} ms")

    @commands.command()
    async def hello(self, ctx):
        await ctx.send(f"Hello {ctx.message.author.name}, howdy?")

    @commands.command(aliases=["ask", "wondering", "forecast"])
    async def question(self, ctx, *, question):

        responses = [   "It is certain.",
                        "It is decidedly so.",
                        "Without a doubt.",
                        "Yes - definitely.",
                        "You may rely on it.",
                        "As I see it, yes.",
                        "Most likely.",
                        "Outlook good.",
                        "Yes.",
                        "Signs point to yes.",
                        "Reply hazy, try again.",
                        "Ask again later.",
                        "Better not tell you now.",
                        "Cannot predict now.",
                        "Concentrate and ask again.",
                        "Don't count on it.",
                        "My reply is no.",
                        "My sources say no.",
                        "Outlook not so good.",
                        "Very doubtful."
                        ]
        await ctx.send(f"Question: {question}\nAnswer: {choice(responses)}")

    # @commands.command(aliases=["info", "infos"], help = "Shows this message")
    # async def help(self, ctx):
    #     help = embed()
    #     await ctx.send(content=None, embed=help)

    @commands.command(aliases=["people"])
    async def users(self, ctx):
        id = bot.get_guild(755003904105906182)
        await ctx.send(f"# of Members: {len(id.members)}")
        for member in id.members:
            await ctx.send(f"{member.name}")

def setup(bot):
    bot.add_cog(Start(bot))