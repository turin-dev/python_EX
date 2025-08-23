"""
최종 프로젝트 스켈레톤.

이 스크립트는 다양한 Cog를 로드하고 AutoShardedBot을 실행하는 기본 예제입니다.
실제 구현에서는 각 Cog 모듈(예: polls.py, economy.py 등)을 cogs 패키지로
구성하고, 해당 모듈에서 `setup` 함수를 제공해야 합니다.
"""

from __future__ import annotations
import os
import asyncio
import discord
from discord.ext import commands


async def main() -> None:
    intents = discord.Intents.default()
    intents.message_content = True
    # 다수의 길드를 지원하기 위해 AutoShardedBot 사용
    bot = commands.AutoShardedBot(command_prefix="!", intents=intents)

    # 로드할 Cog 목록 (모듈 경로)
    extensions = [
        "discord_ex.51.Chapter_51.chapter_51",  # 예: 스케줄링 Cog
        # 실제 프로젝트에서는 'cogs.scheduler', 'cogs.polls', 'cogs.economy', ...
    ]
    for ext in extensions:
        try:
            await bot.load_extension(ext)
        except Exception as e:
            print(f"확장 {ext} 로드 실패: {e}")

    @bot.event
    async def on_ready() -> None:
        print(f"Logged in as {bot.user} (Shard {bot.shard_id}/{bot.shard_count})")

    token = os.getenv("DISCORD_TOKEN")
    if not token:
        raise RuntimeError("DISCORD_TOKEN 환경 변수가 설정되지 않았습니다.")
    await bot.start(token)


if __name__ == "__main__":
    asyncio.run(main())