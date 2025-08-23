from discord.ext import commands

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

@bot.command()
async def hello(ctx):
    await ctx.send(f'안녕하세요, {ctx.author.display_name}님!')

