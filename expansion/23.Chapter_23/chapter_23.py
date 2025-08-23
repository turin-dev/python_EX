"""레이트 리밋과 동시성 관리 예제.

`commands.cooldown`과 `asyncio.Semaphore`를 사용하여 명령어 호출 빈도와 동시에 실행되는 작업 수를 제한하는 방법을 보여 줍니다.
"""

import asyncio
import discord
from discord.ext import commands


bot = commands.Bot(command_prefix="!", intents=discord.Intents.default())


# 사용자별 10초에 2회까지 호출 가능한 명령어
@bot.command()
@commands.cooldown(2, 10, commands.BucketType.user)
async def greet(ctx: commands.Context, *, name: str) -> None:
    """인사를 출력하는 예제.

    동일 사용자가 10초 동안 최대 두 번만 실행할 수 있습니다.
    """
    await ctx.send(f"안녕하세요, {name}님!")


@greet.error
async def greet_error(ctx: commands.Context, error: commands.CommandError) -> None:
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send(f"잠시 후 다시 시도하세요. {error.retry_after:.1f}초 후에 사용할 수 있습니다.")


# 세마포어를 이용해 외부 API 요청 동시수 제한
sem = asyncio.Semaphore(3)


async def fetch_data(url: str) -> str:
    """비동기적으로 데이터를 가져오는 함수. 동시에 3개까지만 실행됩니다."""
    async with sem:
        await asyncio.sleep(1)  # 실제로는 aiohttp 같은 라이브러리를 사용
        return f"데이터: {url}"


@bot.command()
async def query(ctx: commands.Context, *, url: str) -> None:
    """주어진 URL에서 데이터를 가져옵니다."""
    data = await fetch_data(url)
    await ctx.send(data)


if __name__ == "__main__":
    # bot.run("YOUR_TOKEN")
    pass