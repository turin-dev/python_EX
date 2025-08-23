import discord
from discord.ext import commands
from discord import app_commands

bot = commands.Bot(command_prefix='!')

@bot.tree.command(name='choose', description='선택지를 보여줍니다')
@app_commands.describe(option='선택할 과일')
@app_commands.choices(option=[
    app_commands.Choice(name='사과', value=1),
    app_commands.Choice(name='바나나', value=2),
    app_commands.Choice(name='체리', value=3),
])
async def choose(interaction: discord.Interaction, option: app_commands.Choice[int]):
    await interaction.response.send_message(f'선택한 값: {option.name}')

