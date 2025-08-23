"""배포 예제.

환경 변수에서 토큰을 읽어 봇을 실행하는 간단한 스크립트입니다.
"""

import os
import discord
from discord.ext import commands


TOKEN = os.environ.get("DISCORD_TOKEN")

if TOKEN is None:
    raise RuntimeError("DISCORD_TOKEN 환경 변수가 설정되어 있지 않습니다.")

bot = commands.Bot(command_prefix="!", intents=discord.Intents.default())


@bot.event
async def on_ready() -> None:
    print(f"봇 {bot.user} 로 로그인했습니다.")


if __name__ == "__main__":
    bot.run(TOKEN)