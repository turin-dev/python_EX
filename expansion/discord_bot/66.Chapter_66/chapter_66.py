"""APScheduler를 이용한 크론 스케줄링 예제.

이 모듈은 APScheduler를 사용해 매일 특정 시간에 메시지를 보내는
작업을 등록하고, 봇의 `on_ready` 이벤트에서 스케줄러를 시작하는
방법을 보여줍니다.
"""

import os
import discord
from discord.ext import commands
from apscheduler.schedulers.asyncio import AsyncIOScheduler


ANNOUNCE_CHANNEL_ID: int = 123456789012345678


async def daily_message(bot: commands.Bot) -> None:
    """공지 채널에 인사 메시지를 보내는 작업."""
    channel = bot.get_channel(ANNOUNCE_CHANNEL_ID)
    if channel:
        await channel.send("좋은 아침입니다! 오늘도 활기차게 시작하세요.")


def create_bot_with_scheduler() -> commands.Bot:
    bot = commands.Bot(command_prefix="!")
    scheduler = AsyncIOScheduler()

    @bot.event
    async def on_ready() -> None:
        print("Bot is ready")
        if not scheduler.running:
            scheduler.start()
        # 스케줄러에 작업 등록
        scheduler.add_job(daily_message, 'cron', hour=9, minute=0, args=[bot])

    return bot


if __name__ == "__main__":
    bot = create_bot_with_scheduler()
    # bot.run(os.getenv("DISCORD_TOKEN"))

