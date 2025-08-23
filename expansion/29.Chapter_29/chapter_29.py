"""캐시와 샤딩 예제.

이 예제는 메시지 캐시 크기를 제한하고 AutoShardedBot을 사용하는 방법을 보여 줍니다.
"""

import discord
from discord.ext import commands


# 메시지 캐시를 200개로 제한한 봇
bot = commands.AutoShardedBot(command_prefix="!", max_messages=200, intents=discord.Intents.default())


@bot.event
async def on_ready() -> None:
    print(f"봇 준비 완료. 총 {bot.shard_count}개의 샤드 사용 중.")


if __name__ == "__main__":
    # bot.run("YOUR_TOKEN")
    pass