"""설정 관리 예제.

INI 파일과 환경 변수를 읽어 봇을 구성하는 방법을 보여 줍니다.
"""

import configparser
import os
import discord
from discord.ext import commands


# 설정 파일 로드
config = configparser.ConfigParser()
config.read("config.ini", encoding="utf-8")

prefix = config.get("bot", "prefix", fallback="!")
owner_id = config.getint("bot", "owner_id", fallback=0)
weather_key = config.get("api", "weather_key", fallback="")

# 환경 변수에서 토큰 읽기
TOKEN = os.environ.get("DISCORD_TOKEN")
if TOKEN is None:
    raise RuntimeError("DISCORD_TOKEN 환경 변수가 설정되어 있지 않습니다.")

bot = commands.Bot(command_prefix=prefix, intents=discord.Intents.default())


@bot.event
async def on_ready() -> None:
    print(f"봇이 {bot.user} 로 실행 중입니다. 관리자 ID: {owner_id}")


if __name__ == "__main__":
    bot.run(TOKEN)