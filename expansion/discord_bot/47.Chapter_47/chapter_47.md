# 47장 – 샤딩과 병렬 처리

봇이 가입한 길드 수가 많아지면 Discord는 한 프로세스에서 모든 이벤트를 수신하지 못하도록 **샤딩(sharding)**을 요구할 수 있습니다. 샤딩은 여러 개의 연결을 통해 서버와 통신을 분산하는 방식으로, 각 샤드는 전체 길드의 부분 집합을 담당합니다. 또한 CPU를 많이 사용하는 작업을 처리할 때는 병렬성을 고려해야 합니다.

## AutoShardedBot 사용하기

`discord.py`에서는 자동으로 샤드를 관리하는 `commands.AutoShardedBot` 클래스를 제공합니다. 이 클래스는 봇이 속한 길드 수에 따라 권장 샤드 수를 계산하거나, 직접 `shard_count`를 지정하여 인스턴스를 생성할 수 있습니다. 기본 사용법은 다음과 같습니다.

```python
from discord.ext import commands

bot = commands.AutoShardedBot(command_prefix="!", shard_count=2, intents=discord.Intents.all())

@bot.event
async def on_ready():
    print(f"봇 준비 완료 – 샤드 수: {bot.shard_count}")
    # 각 샤드의 길드 수를 출력합니다.
    for shard_id, guilds in bot.shards.items():
        print(f"샤드 {shard_id} – 길드 수: {len([g for g in bot.guilds if g.shard_id == shard_id])}")
```

`shard_count`와 `shard_ids` 매개변수를 사용하면 특정 샤드만 실행할 수 있습니다. 대형 봇에서는 프로세스를 여러 대로 나누고 각 프로세스에 서로 다른 `shard_ids`를 할당합니다. 샤딩을 사용하는 경우 봇 토큰을 Discord 개발자 포털에서 **샤딩 활성화**한 후, 실제 샤드 수에 맞추어 배포해야 합니다.

## 병렬 처리와 GIL

파이썬 스레드는 I/O 바운드 작업에서는 유용하지만, CPU 바운드 작업에서는 **글로벌 인터프리터 락(GIL)**으로 인해 동시에 한 스레드만 바이트코드를 실행할 수 있습니다. 문서에서는 스레드 모듈을 소개하며, I/O 바운드 작업에 적합하지만 CPU 바운드 연산에서는 `multiprocessing`을 사용하는 것이 좋다고 설명합니다【570737854010064†L77-L150】. 따라서 대규모 데이터 처리나 계산을 수행할 때는 `concurrent.futures.ProcessPoolExecutor`를 사용하여 병렬 실행을 분산시키거나 별도의 작업 큐를 구축하는 것이 좋습니다.

## 샤딩과 병렬 처리를 결합한 예제

다음 예제는 `AutoShardedBot`과 병렬 처리 도구를 함께 사용하여 CPU 집중형 작업을 분산 처리하는 방법을 보여줍니다. `asyncio.to_thread`를 사용하면 블로킹 함수를 별도의 스레드에서 실행할 수 있으며, `ProcessPoolExecutor`를 통해 GIL의 영향을 받지 않고 CPU를 사용할 수 있습니다.

```python
import asyncio
from concurrent.futures import ProcessPoolExecutor

def heavy_computation(x: int) -> int:
    # CPU 바운드 작업 예시 (피보나치 수 계산 등)
    if x <= 1:
        return x
    return heavy_computation(x - 1) + heavy_computation(x - 2)


async def calculate_async(loop: asyncio.AbstractEventLoop, n: int) -> int:
    # ProcessPoolExecutor를 사용하여 GIL을 우회합니다.
    with ProcessPoolExecutor() as pool:
        result = await loop.run_in_executor(pool, heavy_computation, n)
    return result


async def setup(bot: commands.AutoShardedBot) -> None:
    @bot.command(name="fib")
    async def fib_cmd(ctx: commands.Context, n: int):
        await ctx.send("계산 중입니다...", delete_after=0)
        loop = asyncio.get_running_loop()
        result = await calculate_async(loop, n)
        await ctx.send(f"fib({n}) = {result}")
```

위 예제에서는 블로킹 함수 `heavy_computation`을 프로세스 풀에서 실행하여 메인 이벤트 루프가 지연되지 않도록 합니다. 이렇게 하면 샤딩으로 분산된 여러 인스턴스에서도 CPU 작업을 효율적으로 처리할 수 있습니다.

## 요약

샤딩은 길드가 많은 봇의 부하를 분산하기 위해 필수적입니다. `AutoShardedBot`을 사용하면 샤드 수와 ID를 쉽게 관리할 수 있고, 봇이 각 샤드에서 처리하는 길드 수를 확인할 수 있습니다. 또한 CPU 집약적인 작업은 `multiprocessing`이나 프로세스 풀을 통해 GIL을 우회해야 하며, `threading`은 주로 I/O 바운드 작업에 적합합니다【570737854010064†L77-L150】.