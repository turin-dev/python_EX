from discord.ext import commands

bot = commands.Bot(command_prefix='!')

@bot.command()
async def add(ctx, a: int, b: int):
    await ctx.send(f'{a} + {b} = {a + b}')

@bot.command()
async def echo(ctx, *, message: str):
    await ctx.send(message)

