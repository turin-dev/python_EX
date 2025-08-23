"""쿨다운과 동시 실행 제한 예제.

이 모듈은 쿨다운을 적용한 명령과 동시에 하나만 실행되는 명령을
정의한 봇을 제공합니다.
"""

import discord
from discord.ext import commands


def create_bot() -> commands.Bot:
    intents = discord.Intents.default()
    intents.message_content = True
    bot = commands.Bot(command_prefix="!", intents=intents)

    @commands.cooldown(1, 10, commands.BucketType.user)
    @bot.command(name="hello")
    async def hello(ctx: commands.Context) -> None:
        await ctx.send("안녕하세요!")

    @hello.error
    async def hello_error(ctx: commands.Context, error: commands.CommandError) -> None:
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(f"잠시만 기다려 주세요. {error.retry_after:.1f}초 후 다시 시도할 수 있습니다.")

    @commands.max_concurrency(1, per=commands.BucketType.guild)
    @bot.command(name="vote")
    async def vote(ctx: commands.Context) -> None:
        await ctx.send("투표를 시작합니다! 10초 후 종료됩니다.")
        # 여기에서 실제 투표 로직을 구현합니다.
        await asyncio.sleep(10)
        await ctx.send("투표가 종료되었습니다.")

    return bot


if __name__ == "__main__":
    import os
    import asyncio
    bot = create_bot()
    @bot.event
    async def on_ready() -> None:
        print("Bot ready with cooldown and concurrency controls")
    # bot.run(os.getenv("DISCORD_TOKEN"))

