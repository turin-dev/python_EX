from discord.ext import commands

class MyCog(commands.Cog, name='맞춤 코그'):
    def __init__(self, bot):
        self.bot = bot

    def cog_unload(self):
        print('코그 언로드!')

    def cog_check(self, ctx):
        # 코그 전체 체크: 길드에서만 사용
        return ctx.guild is not None

    @commands.command()
    async def ping(self, ctx):
        await ctx.send('pong!')

