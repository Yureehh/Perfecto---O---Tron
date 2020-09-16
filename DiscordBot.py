import discord
import time
import asyncio
from datetime import datetime
from discord.ext import commands, tasks
from random import choice
from itertools import cycle
import os

def read_token():
    with open("token.txt", "r") as f:
        lines = f.readlines()
        return lines[0].strip()


MINUTES_TO_WAIT = 1
messages = joined = 0
status = cycle(["League of Lol", "with your mind", "with your fate", "with your secrets", "Fortine is for kids", "CS:GO is old", "Valoraahahahahnt","with your emotions"])
token = read_token()

bot = commands.Bot(command_prefix='.')

bot.remove_command('help')

async def update_stats():
    global messages, joined

    while not bot.is_closed():
        try:
            now = datetime.now()
            current_time = now.strftime("%D %H:%M:%S")

            with open("stats.txt", "a+") as f:
                f.write(f"Time: {current_time}, Messages: {messages}, Members Joined: {joined}\n")

            messages = 0
            joined = 0
            await asyncio.sleep(MINUTES_TO_WAIT * 60)

        except Exception as e:
            print(e)
            await asyncio.sleep(MINUTES_TO_WAIT * 60)

@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.online )
    changeStatus.start()
    bot.loop.create_task(update_stats())

    print("Bot launched")

@tasks.loop(seconds = MINUTES_TO_WAIT * 60)
async def changeStatus():
    await bot.change_presence(activity = discord.Game(next(status)))



@bot.event
async def on_member_update(before, after):
    n = after.nick
    if n:
        if n.lower().count("Yureeh") > 0:
            await after.edit(nick = "Te piacess")

@bot.event
async def on_member_join(member):
    global joined
    joined += 1
    for channel in member.guild.channels:
        print(type(channel))
        if str(channel) == "welcome":
            await channel.send(f"""Welcome to the server {member.mention}""")

# @bot.event
# async def on_member_remove(member):
#     print(f"{member} has left the {member.}")

@bot.event
async def on_message(message):
    global messages
    messages += 1
    await bot.process_commands(message)

@bot.command()
async def ping(ctx):
    await ctx.send(f"Your ping is {round(bot.latency * 1000)} ms")

@bot.command()
async def hello(ctx):
    await ctx.send(f"Hello {ctx.message.author.name}, howdy?")

@bot.command(aliases=["ask", "wondering", "forecast"])
async def question(ctx, *, question):

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

@bot.command(aliases=["info", "infos"], help = "Shows this message")
async def help(ctx):
    help = embed()
    await ctx.send(content=None, embed=help)

@bot.command(aliases=["people"])
async def users(ctx):
    id = bot.get_guild(755003904105906182)
    await ctx.send(f"# of Members: {len(id.members)}")
    for member in id.members:
        await ctx.send(f"{member.name}")

def embed():
    embed = discord.Embed(title="Help on BOT", description="Some useful commands")
    embed.add_field(name=".help",       value="shows this message")
    embed.add_field(name=".hello",      value="Greets the user")
    embed.add_field(name=".users",      value="Prints number and names of all the users")
    embed.add_field(name=".question",   value="Answers randomly to the user question")
    embed.add_field(name=".ping",       value="return the user ping")
    return embed

@bot.command()
@commands.has_permissions(manage_messages = True)
async def clear(ctx, amount = 5):
    await ctx.channel.purge(limit = amount)

#the asterisc takes all the parameters passed after the command and puts it into reason
@bot.command()
@commands.has_permissions(ban_members=True)
async def kick(ctx, member : discord.Member, *, reason = None):
    await member.kick(reason = reason)

@bot.command()
async def ban(ctx, member : discord.Member, *, reason = None):
    await member.ban(reason = reason)


@bot.command(name = "sban")
async def unban(ctx, *, member):
    bannedUsers = await ctx.guild.bans()
    memberName, memberDiscriminator = member.split("#")

    for banned in bannedUsers:
        user = banned.user

        if (user.name, user.discriminator) == (memberName, memberDiscriminator):
            await ctx.guild.unban(user)
            await ctx.send(f"Unbanned {user.mention}")
            return



# @bot.command()
# async def load(ctx, extension):
#     bot.load_extension(f"cogs.{extension}")

# @bot.command()
# async def unload(ctx, extension):
#     bot.unload_extension(f"cogs.{extension}")

# @bot.command()
# async def reload(ctx, extension):
#     bot.unload_extension(f"cogs.{extension}")
#     bot.load_extension(f"cogs.{extension}")

# for filename in os.listdir("./cogs"):
#     if filename.endswith(".py"):
#         bot.load_extension(f"cogs.{filename[:-3]}")

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please pass in all required arguments")

# @clear.error
# async def clear_error(ctx, error):
#     if isinstance(error, commands.MissingRequiredArgument):
#         await ctx.send("please specify an amount of messages to delete")

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("invalid command used")

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send(f"{ctx.author.name} is not allowed to use that command")


bot.run(token)