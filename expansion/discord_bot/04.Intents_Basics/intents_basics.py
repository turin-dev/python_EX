import discord

# 메시지와 길드 이벤트만 수신하는 인텐트
intents = discord.Intents(messages=True, guilds=True)

bot = discord.Client(intents=intents)

