import discord
from discord.ext import commands, tasks
import os

#gets the token throught environments variables from heroku
token = "NzU1MDA0ODI3NzI5Mzk1NzMy.X18_Cg.kK2qN06rp4yyOT4_U5VFpnhjgq0"
#token = os.environ.get("BOT_TOKEN")


bot = commands.Bot(command_prefix='.')

bot.remove_command('help')

def embed():
    embed = discord.Embed(title="Help on BOT", description="Some useful commands")
    embed.add_field(name=".help",       value="shows this message")
    embed.add_field(name=".hello",      value="Greets the user")
    embed.add_field(name=".users",      value="Prints number and names of all the users")
    embed.add_field(name=".question",   value="Answers randomly to the user question")
    embed.add_field(name=".ping",       value="return the user ping")
    return embed







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

@bot.command(name = "load cogs", aliases = ["load all cogs", "load all"] )
async def load_all_cogs(ctx):
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            try:
                bot.load_extension(f"cogs.{filename[:-3]}")
            except commands.ExtensionAlreadyLoaded:
                await ctx.send(f"Cog {filename} is already loaded")

@bot.command()
async def check_cogs(ctx, cog_name):
    try:
        bot.load_extension(f"cogs.{cog_name}")
    except commands.ExtensionAlreadyLoaded:
        await ctx.send("Cog is loaded")
    except commands.ExtensionNotFound:
        await ctx.send("Cog not found")
    else:
        await ctx.send("Cog is unloaded")
        bot.unload_extension(f"cogs.{cog_name}")

bot.run(token)