from discord.ext import commands

bot = commands.Bot(command_prefix='!')

@bot.command()
@commands.has_permissions(manage_guild=True)
async def announce(ctx, *, msg):
    await ctx.send(f'공지: {msg}')

