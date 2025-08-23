import discord
from discord.ext import commands
from discord import app_commands

bot = commands.Bot(command_prefix='!')

@bot.tree.context_menu(name='유저 정보 보기')
async def view_profile(interaction: discord.Interaction, member: discord.Member):
    await interaction.response.send_message(f'{member.display_name}의 ID: {member.id}')

@bot.tree.context_menu(name='메시지 길이')
async def message_length(interaction: discord.Interaction, message: discord.Message):
    await interaction.response.send_message(f'이 메시지의 길이: {len(message.content)}')

