"""작업 스케줄링 고급 예제.

하루에 두 번 메시지를 보내고, 실행 간격을 동적으로 변경하는 루프를 구현합니다.
"""

import datetime
import discord
from discord.ext import commands, tasks


bot = commands.Bot(command_prefix="!", intents=discord.Intents.default())


@tasks.loop(time=[datetime.time(hour=9, minute=0), datetime.time(hour=18, minute=0)])
async def daily_announcements() -> None:
    channel = bot.get_channel(123456789012345678)
    if channel:
        await channel.send("하루 두 번의 공지입니다!")


@daily_announcements.before_loop
async def before_announcements() -> None:
    await bot.wait_until_ready()


# 실행 횟수와 간격 변경 예제
@tasks.loop(seconds=10, count=5)
async def limited_task() -> None:
    print(f"실행 번호: {limited_task.current_loop + 1}")
    # 4번째 실행 후 간격을 60초로 변경
    if limited_task.current_loop == 3:
        limited_task.change_interval(seconds=60)


@limited_task.after_loop
async def after_limited_task() -> None:
    print("루프가 완료되었습니다!")


if __name__ == "__main__":
    # bot.run("YOUR_TOKEN")
    pass