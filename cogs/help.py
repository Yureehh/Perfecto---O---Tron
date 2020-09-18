import discord
from discord.ext import commands
import asyncio

#toimpove: avoid the possibility to call another .help while one is already ongoing toherwise if you react to one both of them change

class Helper(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name = "help", aliases = ["Help", "info", "Info"], help = """Can be used in 3 ways:\n
                                                                                    1️⃣ without argument and creates a message you can react to switch pages and see all the commands of all the classes
                                                                                    2️⃣ passing as an argument a class of commands and will show all the commands of that class
                                                                                    3️⃣ passing the name of a command and will show only that specific command documentation""")
    async def helpFunction(self, ctx, text = None):

        all_cogs = [c for c in self.bot.cogs]
        all_commands = [c.name for c in self.bot.commands]
        color = [discord.Colour.blue(), discord.Colour.green(), discord.Colour.purple(), discord.Colour.orange() ]

        if text == None:
            embed = discord.Embed(title="Do you need help? 🆘", description = """Here you have a list of commands separated per cog
                                                                                React to this message to change page!""", color=color[0])
            embed.add_field(name = "`Bot creator`", value = "Yureeh™️", )
            embed.add_field(name = "`Contact Me`", value = """If you have any question or suggestion you can write me on discord: Yureeh#4871
                                                            or on the bot github page: https://github.com/Yureehh/Perfecto---O---Tron""", )
            #embed2 = discord.Embed(title="Do you need help?", description = "list of commands separated per cog", color=color2)
            pages = [embed]
            for cog in all_cogs:
                cogCommands = [c for c in self.bot.get_cog(cog).get_commands() if await c.can_run(ctx) and not c.hidden]
                if len(cogCommands) > 0:
                    page = discord.Embed(title = cog, description = f"Help with the `{cog}` commands :gear:", color = color[1], )
                    for c in cogCommands:
                        if c.help == None:
                            message = 'There is no documentation for this command'
                        else:
                            message = c.help
                        page.add_field(name=f"`{c.name}`", value=message, )
                    pages.append(page)
            message = await ctx.send(embed=embed)

            await message.add_reaction('\u23ee')
            await message.add_reaction('\u25c0')
            await message.add_reaction('\u25b6')
            await message.add_reaction('\u23ed')

            i = 0
            emoji = ""

            while True:
                if emoji=='\u23ee':
                    i=0
                    await message.edit(embed=pages[i])
                if emoji=='\u25c0':
                    if i>0:
                        i-=1
                    else:
                        i = len(pages) - 1
                    await message.edit(embed=pages[i])
                if emoji=='\u25b6':
                    if i< len(pages) - 1:
                        i+=1
                    else:
                        i = 0
                    await message.edit(embed=pages[i])
                if emoji=='\u23ed':
                    i=len(pages)-1
                    await message.edit(embed=pages[i])

                def check(reaction, user):
                    return ctx.message.author == user and ctx.message.channel == reaction.message.channel
                    # return ( reaction.message.channel == ctx.message.channel
                    #          and ( str(reaction.emoji) == '\u23ee' or  str(reaction.emoji) == "\u25c0"
                    #          or str(reaction.emoji) == "\u25b6" or str(reaction.emoji) == "\u23ed" ) )

                try:
                    reaction,user = await self.bot.wait_for('reaction_add',timeout = 30,check=check)
                    emoji=str(reaction.emoji)

                    await message.remove_reaction(emoji,user)
                except asyncio.TimeoutError:
                    await message.delete()
                    break

            await bot.clear_reactions(message)

        elif text in all_cogs:
            cogCommands = [c for c in self.bot.get_cog(text).get_commands() if await c.can_run(ctx) and not c.hidden]
            if len(cogCommands) > 0:
                embed = discord.Embed(title="Do you need help?", description = f"List of the commands of the cog: `{text}` :gear:", color=color[2])
                for c in cogCommands:
                    if c.help == None:
                        message = 'There is no documentation for this command'
                    else:
                        message = c.help
                    embed.add_field(name=f"`{c.name}", value=message, )
                message = await ctx.send(embed=embed)
                await message.delete(delay = 30)
            else:
                await ctx.send("This cog has no commands")

        elif text in all_commands:
            c = self.bot.get_command(text)
            if c.name == text:
                command = c
            embed = discord.Embed(title="Do you need help?", description = f"Description of the command: `{text}` :gear:", color=color[3])
            if c.help == None:
                message = 'There is no documentation for this command'
            else:
                message = c.help
            embed.add_field(name=f"`{c.name}`", value=message, )
            message = await ctx.send(embed=embed)
            await message.delete(delay = 30)

def setup(bot):
    bot.add_cog(Helper(bot))