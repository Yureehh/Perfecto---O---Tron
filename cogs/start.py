import discord
from discord.ext import commands,tasks
from datetime import datetime
import asyncio
from itertools import cycle

#number of minutes used at timer for loops
MINUTES_TO_WAIT = 1

#in the brackets there's the class you are extending
class Start(commands.Cog):

    def __init__(self, bot, messages=0, joined=0):
        self.bot = bot
        self.messages = messages
        self.joined = joined
        #Status the bot will cicle. All of them are memes of course
        self.status = cycle(["League of Lol", "with your mind", "with your fate", "with your secrets", "Fortine is for kids", "CS:GO is old", "Valoraahahahahnt","with your emotions"])


    async def update_stats(self):

        while not bot.is_closed():
            try:
                now = datetime.now()
                current_time = now.strftime("%D %H:%M:%S")

                with open("stats.txt", "a+") as f:
                    f.write(f"Time: {current_time}, Messages: {self.messages}, Members Joined: {self.joined}\n")

                self.messages = 0
                self.joined = 0
                await asyncio.sleep(MINUTES_TO_WAIT * 60)

            except Exception as e:
                print(e)
                await asyncio.sleep(MINUTES_TO_WAIT * 60)

    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.change_presence(status=discord.Status.online )
        self.changeStatus.start()
        self.bot.loop.create_task(update_stats())
        print("Bot launched")

    @tasks.loop(seconds = MINUTES_TO_WAIT * 60)
    async def changeStatus(self):
        await self.bot.change_presence(activity = discord.Game(next(self.status)))

    @commands.Cog.listener()
    async def on_message(self, message):
        self.messages += 1
        await self.bot.process_commands(message)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        self.joined += 1
        for channel in member.guild.channels:
            if str(channel) == "welcome":
                await channel.send(f"Welcome to the server {member.mention}", file = discord.File("images/welcome.jpg"))

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        message = f"Bye bye {member.mention}, looking forward to your return"
        for channel in member.guild.channels:
            if str(channel) == "welcome" or str(channel) == "goodbyes":
                await channel.send(f"{member.mention} left the server", file = discord.File("images/missYou.jpg"))

def setup(bot):
    bot.add_cog(Start(bot))