from discord.ext import commands

class GreetingCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = member.guild.system_channel
        if channel:
            await channel.send(f'{member.mention}님, 환영합니다!')

    @commands.command()
    async def hello(self, ctx):
        await ctx.send('안녕하세요!')

# 등록
bot = commands.Bot(command_prefix='!')
bot.add_cog(GreetingCog(bot))

