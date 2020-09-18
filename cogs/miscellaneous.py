import discord
from discord.ext import commands
from random import choice, randint

class Misc(commands.Cog):

    def __init__(self, bot):
        self.bot = bot


    @commands.command(name = "ping", aliases = ["lag", "7mega", "latency"], help = "returns the user ping")
    async def ping(self, ctx):
        await ctx.send(f"Your ping is {round(self.bot.latency * 1000)} ms")

    @commands.command(name = "hello", aliases = ["greetings", "hi", "howdy", "gm", "ga"], help = "greets the user" )
    async def greeting(self, ctx):
        await ctx.send(f"Hello {ctx.message.author.name}, howdy?", file = discord.File("images/gm.gif"))

    @commands.command(name = "question", aliases=["ask", "wondering", "forecast"], help = "answers randomly to the user question")
    async def randomAnswer(self, ctx, *, question):

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

    @commands.command(name = "users", aliases=["people", "members"], help = "returns the number and the names of every user belonging to the server")
    async def usersOfTheChannel(self, ctx):
        id = bot.get_guild(755003904105906182)
        await ctx.send(f"# of Members: {len(id.members)}")
        for member in id.members:
            await ctx.send(f"{member.name}")
    @commands.command(name = "roll6", aliases = ["rollD6", "rollDice6"], help = "Rolls typical dice")
    async def rollD6(self, ctx):
        await ctx.send(f"You rolled a {randint(1,6)}")

    @commands.command(name = "roll20", aliases = ["rollD20", "rollDice20"], help = "Rolls a d20")
    async def rollD20(self, ctx):
        await ctx.send(f"You rolled a {randint(1,20)}")

    @commands.command(name = "roll", aliases = ["rollBetween", "rollIn"], help = "Rolls a custom dice")
    async def rollBetween(self, ctx, low=1, high=6):
        await ctx.send(f"You rolled a {randint(low,high)}")

def setup(bot):
    bot.add_cog(Misc(bot))