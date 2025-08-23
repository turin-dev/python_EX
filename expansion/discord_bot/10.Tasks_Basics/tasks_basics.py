from discord.ext import tasks, commands

class Counter(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.counter = 0
        self.printer.start()

    def cog_unload(self):
        self.printer.cancel()

    @tasks.loop(seconds=5.0)
    async def printer(self):
        print(self.counter)
        self.counter += 1

