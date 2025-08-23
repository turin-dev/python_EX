"""Docker 및 CI/CD 배포 예제.

이 모듈에서는 환경 변수로 토큰을 읽어 봇을 실행하는 기본적인
구성을 보여줍니다. 실제 배포에서는 Dockerfile에서 이미지를
빌드하고, GitHub Actions와 같이 CI/CD 파이프라인을 사용해 자동
배포를 수행합니다.
"""

import os
import discord
from discord.ext import commands


def main() -> None:
    """환경 변수에서 토큰을 읽어 봇을 실행합니다."""
    token = os.getenv("DISCORD_TOKEN")
    if not token:
        raise RuntimeError("DISCORD_TOKEN 환경 변수가 설정되지 않았습니다")
    intents = discord.Intents.default()
    intents.message_content = True
    bot = commands.Bot(command_prefix="!", intents=intents)

    @bot.event
    async def on_ready() -> None:
        print(f"Logged in as {bot.user}")

    bot.run(token)


if __name__ == "__main__":
    main()

