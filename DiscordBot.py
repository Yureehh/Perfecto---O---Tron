import discord
from discord.ext import commands, tasks
import os

# gets the token throught environments variables from heroku
token = os.environ.get("BOT_TOKEN")

# def read_token():
#     with open("token.txt", "r") as f:
#         lines = f.readlines()
#         return lines[0].strip()

#gets the token from a file if i am personally hosting the bot
# token = read_token()



bot = commands.Bot(command_prefix='.', help_command = None)

@bot.command(name = "loadAll", aliases = ["loadAllCogs", "loadEverything", "massLoad"])
async def loadAllCogs(ctx):
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            try:
                bot.load_extension(f"cogs.{filename[:-3]}")
                await ctx.send(f'{filename[:-3]} successfully loaded')
            except commands.ExtensionAlreadyLoaded:
                await ctx.send(f"Cog {filename[:-3]} is already loaded")


@bot.command(name = "unloadAll", aliases = ["unloadAllCogs", "unloadEverything", "massUnload"])
async def unloadAllCogs(ctx):
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            try:
                bot.unload_extension(f"cogs.{filename[:-3]}")
                await ctx.send(f'{filename[:-3]} successfully unloaded')
            except commands.ExtensionAlreadyLoaded:
                await ctx.send(f"Cog {filename[:-3]} is not loaded")


@bot.command()
async def load(ctx, extension):
    bot.load_extension(f"cogs.{extension}")
    print(f'{extension} successfully loaded')

@load.error
async def load_error(ctx, error):
    await ctx.send(f"The following error occured:```\n{error}\n```")

@bot.command()
async def unload(ctx, extension):
    bot.unload_extension(f"cogs.{extension}")
    await print(f'{extension} successfully un-loaded')

@unload.error
async def unload_error(ctx, error):
 await ctx.send(f"The following error occured:```\n{error}\n```")

@bot.command()
async def reload(ctx, extension):
    bot.unload_extension(f"cogs.{extension}")
    bot.load_extension(f"cogs.{extension}")
    print(f'{extension} successfully re-loaded')

@reload.error
async def unload_error(ctx, error):
 await ctx.send(f"The following error occured:```\n{error}\n```")


@bot.command(name = "checkCog", aliases = ["checkOnlineCog"])
async def checkOnlineCog(ctx, cog_name):
    try:
        bot.load_extension(f"cogs.{cog_name}")
    except commands.ExtensionAlreadyLoaded:
        await ctx.send("Cog is loaded")
    except commands.ExtensionNotFound:
        await ctx.send("Cog not found")
    else:
        await ctx.send("Cog is unloaded")

@bot.command(name = "checkCogs", aliases = ["checkOnlineCogs"])
async def checkOnlineCogs(ctx):
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            try:
                bot.load_extension(f"cogs.{filename}")
            except commands.ExtensionAlreadyLoaded:
                await ctx.send("Cog is loaded")
            except commands.ExtensionNotFound:
                await ctx.send("Cog not found")
            else:
                await ctx.send("Cog is unloaded")

for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        try:
            bot.load_extension(f"cogs.{filename[:-3]}")
        except Exception as e:
            print(e)

bot.run(token)