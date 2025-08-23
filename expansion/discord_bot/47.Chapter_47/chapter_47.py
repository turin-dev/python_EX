"""
47장 – 샤딩과 병렬 처리 예제

이 모듈은 AutoShardedBot을 사용하여 길드를 분산 처리하는 방법과 CPU 바운드 작업을
ProcessPoolExecutor로 처리하는 방법을 보여준다.
"""

import asyncio
from concurrent.futures import ProcessPoolExecutor

import discord
from discord.ext import commands


def heavy_computation(x: int) -> int:
    """CPU 바운드 계산을 수행하는 재귀 함수 (예: 피보나치)."""
    if x <= 1:
        return x
    return heavy_computation(x - 1) + heavy_computation(x - 2)


async def calculate_async(loop: asyncio.AbstractEventLoop, n: int) -> int:
    """ProcessPoolExecutor를 이용하여 CPU 작업을 비동기적으로 수행한다."""
    with ProcessPoolExecutor() as pool:
        return await loop.run_in_executor(pool, heavy_computation, n)


async def setup(bot: commands.AutoShardedBot) -> None:
    """샤딩과 병렬 처리 예제 명령을 등록한다."""

    @bot.event
    async def on_ready() -> None:
        print(f"샤드 수: {bot.shard_count}")
        # 각 샤드가 처리하는 길드 수 출력
        for shard_id in range(bot.shard_count or 1):
            guild_count = len([g for g in bot.guilds if g.shard_id == shard_id])
            print(f"샤드 {shard_id}: {guild_count} 길드")

    @bot.command(name="fib")
    async def fib_cmd(ctx: commands.Context, n: int) -> None:
        """ProcessPool을 사용하여 피보나치 수를 계산한다."""
        await ctx.send("계산 중입니다...", delete_after=0)
        loop = asyncio.get_running_loop()
        result = await calculate_async(loop, n)
        await ctx.send(f"fib({n}) = {result}")

