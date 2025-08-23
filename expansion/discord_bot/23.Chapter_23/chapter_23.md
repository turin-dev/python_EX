# 23장 – 레이트 리밋과 동시성 관리

Discord API는 남용을 방지하기 위해 요청 빈도를 제한합니다. `discord.py` 라이브러리는 라이브러리 내부적으로 이러한 **레이트 리밋(rate limit)** 을 자동으로 처리하지만, 개발자는 명령어 호출을 사용자가 과도하게 반복하지 않도록 추가적인 제한을 걸 수 있습니다. 또한 비동기 코드를 작성할 때는 동시에 실행되는 작업 수를 적절히 제어해야 서버에 과도한 부하를 주지 않습니다.

## 명령어 쿨다운 설정

명령어에 쿨다운(cooldown)을 적용하면 일정 시간 동안 호출 횟수를 제한할 수 있습니다. `@commands.cooldown(rate, per, type)` 데코레이터를 사용하며, `type` 매개변수로 `BucketType.user`(사용자별), `BucketType.guild`(서버별), `BucketType.channel`(채널별) 등을 지정합니다.

```python
from discord.ext import commands

bot = commands.Bot(command_prefix="!")

@bot.command()
@commands.cooldown(3, 10, commands.BucketType.user)
async def ping(ctx):
    """3회까지 10초당 호출할 수 있는 ping 명령어"""
    await ctx.send("퐁!")

@ping.error
async def ping_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send(f"잠시 후 다시 시도하세요. 남은 시간: {error.retry_after:.1f}초")
```

이렇게 하면 사용자는 10초에 3회까지만 `!ping`을 호출할 수 있으며, 초과 시 남은 시간을 안내합니다. 필요하다면 `commands.MaxConcurrency`를 이용해 동시에 실행되는 인스턴스 수를 제한할 수 있습니다.

## API 호출 동시성 관리

외부 API나 I/O 연산을 수행할 때는 Python의 `asyncio.Semaphore`를 사용해 최대 동시 실행 수를 제한할 수 있습니다. 예를 들어 HTTP 요청을 병렬로 처리하되 동시에 5개까지만 허용하려면 다음과 같이 작성합니다.

```python
import asyncio
import aiohttp

sem = asyncio.Semaphore(5)

async def fetch(url: str) -> str:
    async with sem:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                return await resp.text()
```

`discord.py` 명령어 내부에서 이러한 함수를 호출할 때는 `await`를 사용해 응답을 받을 수 있으며, 동시 요청 수를 초과하지 않습니다. 또한 반복 작업을 스케줄링할 때는 `@tasks.loop` 데코레이터를 사용하여 적절한 간격을 두고 실행하도록 해야 하며, 예외 발생 시 자동으로 재시작할 수 있도록 `add_exception_type()`을 활용합니다【230406618874054†L25-L36】.

## 요약

레이트 리밋을 준수하는 것은 Discord API를 안정적으로 사용하는 데 필수적입니다. `@commands.cooldown`과 `commands.MaxConcurrency`를 통해 명령어 호출을 제한하고, 세마포어와 주기적 작업 루프를 이용해 비동기 작업의 동시성을 관리하세요. 이는 서버 자원을 보호하고 사용자 경험을 향상시키는 데 도움이 됩니다.

