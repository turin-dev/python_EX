import discord
from discord.ext import commands
from discord import app_commands

class MyBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix='!', intents=discord.Intents.all())
    async def setup_hook(self):
        # 슬래시 커맨드 동기화
        await self.tree.sync()

# 슬래시 커맨드 등록
bot = MyBot()
@bot.tree.command(name='hello', description='인사 커맨드')
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message('안녕하세요!')

