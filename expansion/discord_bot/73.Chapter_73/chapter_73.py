"""
동시성 도구 사용 예제.

이 스크립트는 `asyncio.Lock`, `asyncio.Semaphore`, `asyncio.Queue`를 사용하여
디스코드 봇에서 경쟁 상태를 방지하고 외부 API 호출 수를 제한하는 예를 보여줍니다.

- CounterCog: 락을 사용해 공유 카운터를 안전하게 증가
- DataFetchCog: 세마포어를 이용해 API 요청 병렬 수 제한
- QueueCog: 명령으로 작업을 큐에 추가하고, 백그라운드 루프에서 큐를 소비

또한 `max_concurrency` 데코레이터로 명령 동시 실행을 제한하는 예를 포함합니다.
"""

from __future__ import annotations
import asyncio
from typing import Optional

import discord
from discord.ext import commands, tasks

try:
    import aiohttp
except ImportError:
    aiohttp = None


class CounterCog(commands.Cog):
    """락을 사용한 카운터 갱신."""
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.lock = asyncio.Lock()
        self.counter = 0

    @commands.command(name="increment")
    async def increment_counter(self, ctx: commands.Context) -> None:
        async with self.lock:
            self.counter += 1
            await ctx.send(f"카운터 값: {self.counter}")


class DataFetchCog(commands.Cog):
    """세마포어를 사용한 외부 API 요청 제한."""
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.sem = asyncio.Semaphore(3)  # 동시에 3개 요청

    async def fetch_json(self, session: aiohttp.ClientSession, url: str) -> Optional[dict]:
        async with self.sem:
            async with session.get(url) as resp:
                return await resp.json()

    @commands.command(name="fetch")
    async def fetch_multiple(self, ctx: commands.Context, *urls: str) -> None:
        if aiohttp is None:
            return await ctx.send("aiohttp가 설치되지 않았습니다.")
        async with aiohttp.ClientSession() as session:
            tasks = [asyncio.create_task(self.fetch_json(session, u)) for u in urls]
            results = await asyncio.gather(*tasks)
        await ctx.send(f"{len(results)}개의 응답을 받았습니다.")


class QueueCog(commands.Cog):
    """작업 큐와 소비 루프."""
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.queue: asyncio.Queue[str] = asyncio.Queue()
        self.process_loop.start()

    @commands.command(name="enqueue")
    async def enqueue_job(self, ctx: commands.Context, url: str) -> None:
        await self.queue.put(url)
        await ctx.send(f"작업 추가: {url}")

    @tasks.loop(seconds=1.0)
    async def process_loop(self) -> None:
        while not self.queue.empty():
            url = await self.queue.get()
            # 실제 처리: 예를 들어 다운로드나 파싱
            print(f"처리 중: {url}")
            self.queue.task_done()

    @process_loop.before_loop
    async def before_process_loop(self) -> None:
        await self.bot.wait_until_ready()


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(CounterCog(bot))
    await bot.add_cog(DataFetchCog(bot))
    await bot.add_cog(QueueCog(bot))

    @bot.command(name="exclusive")
    @commands.max_concurrency(1, commands.BucketType.guild, wait=True)
    async def exclusive(ctx: commands.Context) -> None:
        """한 번에 한 길드에서만 실행될 수 있는 명령."""
        await ctx.send("10초 동안 다른 호출을 차단합니다...")
        await asyncio.sleep(10)
        await ctx.send("exclusive 명령이 종료되었습니다.")