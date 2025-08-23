import discord
from discord.ext import commands
from discord import app_commands

bot = commands.Bot(command_prefix='!')

@bot.tree.command(name='echo', description='메시지를 다시 보냅니다')
@app_commands.describe(content='응답할 메시지')
async def echo(interaction: discord.Interaction, content: str):
    await interaction.response.send_message(content)

@bot.event
async def on_ready():
    await bot.tree.sync()  # 글로벌 동기화
    print('봇 준비 완료')

