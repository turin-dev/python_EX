# 동시성 도구: 세마포어, 락, 큐

디스코드 봇이 여러 사용자의 요청을 동시에 처리할 때는 비동기 함수를 남발하면
안 됩니다. 외부 API의 호출 제한을 초과하거나, 공유 리소스를 엉망으로 만들 수
있습니다. **동시성 제어**를 위해 `asyncio`가 제공하는 `Lock`, `Semaphore`,
`Queue`를 적절히 사용하면 이러한 문제를 완화할 수 있습니다. 또한 `discord.py`
명령 프레임워크에는 `commands.max_concurrency`가 있어 명령별로 동시 실행을
제한할 수 있습니다【230406618874054†L160-L210】.

## `asyncio.Lock` — 상호배제

락(Lock)은 한 번에 하나의 작업만 임계 구역을 실행하도록 보장합니다. 예를 들어
파일 쓰기나 메모리 내 카운터 업데이트 등 경쟁 상태가 발생할 수 있는 코드에
사용합니다.

```python
lock = asyncio.Lock()

@bot.command()
async def increment(ctx):
    async with lock:
        # 공유 변수 증가
        ctx.bot.counter = getattr(ctx.bot, "counter", 0) + 1
        await ctx.send(f"카운터: {ctx.bot.counter}")
```

`async with lock:` 구문은 락을 획득하고 해제하는 과정을 자동으로 처리합니다.
락이 이미 다른 작업에 의해 획득된 경우 그 해제가 될 때까지 대기합니다.

## `asyncio.Semaphore` — 병렬 작업 제한

세마포어(Semaphore)는 동시에 실행할 수 있는 작업 수를 제한합니다. 예를 들어
외부 API에 1초당 5번 이상 호출하면 안 되는 경우, 세마포어를 통해 호출 수를
제어할 수 있습니다.

```python
api_sem = asyncio.Semaphore(5)  # 동시에 5개의 작업만 허용

async def fetch_data(session, url):
    async with api_sem:
        async with session.get(url) as resp:
            return await resp.json()

@bot.command()
async def multi_fetch(ctx, *urls):
    async with aiohttp.ClientSession() as session:
        tasks = [asyncio.create_task(fetch_data(session, url)) for url in urls]
        results = await asyncio.gather(*tasks)
    await ctx.send(f"{len(results)}개의 응답을 받았습니다.")
```

세마포어는 임계 구역 대신 **병렬 요청 수**를 제한하는 데 쓰이며, 획득 후
해제해야 다른 요청이 실행됩니다.

## `asyncio.Queue` — 작업 대기열

큐는 생산자-소비자 패턴을 구현할 때 유용합니다. 작업을 큐에 넣는 생산자와
작업을 처리하는 소비자를 분리하면, 봇은 버스트 트래픽을 버퍼링하며 안정적으로
작업을 처리할 수 있습니다.

```python
task_queue: asyncio.Queue[str] = asyncio.Queue()

# 생산자: 명령을 통해 작업 추가
@bot.command()
async def add_job(ctx, url: str):
    await task_queue.put(url)
    await ctx.send(f"작업 대기열에 추가: {url}")

# 소비자: 백그라운드 태스크로 큐를 처리
@tasks.loop(seconds=1.0)
async def process_queue():
    while not task_queue.empty():
        url = await task_queue.get()
        # 실제 작업 수행 (예: 다운로드)
        print(f"처리 중: {url}")
        task_queue.task_done()

process_queue.start()
```

큐를 사용할 때는 `task_done()`을 호출하여 작업 완료를 표시해야 합니다. 또한
`queue.join()`을 이용해 모든 작업이 완료될 때까지 기다릴 수 있습니다.

## `commands.max_concurrency` — 명령 동시 실행 제한

`discord.py` 명령 데코레이터는 `max_concurrency` 옵션으로 동시에 실행할 수
있는 명령 호출 수를 제한합니다. 예를 들어 특정 명령이 한 서버에서 한 번에
하나만 실행되도록 하려면 다음과 같이 설정합니다:

```python
@bot.command()
@commands.max_concurrency(1, commands.BucketType.guild, wait=True)
async def sensitive(ctx):
    await ctx.send("중요 작업 시작...")
    await asyncio.sleep(10)
    await ctx.send("작업 완료!")
```

`wait=True` 옵션은 다른 호출이 대기하도록 하고, `False`이면 즉시 오류를
발생시킵니다. 버킷 유형을 `BucketType.member`로 변경하면 사용자별로 제한을
둘 수 있습니다.

---

이번 장에서는 락과 세마포어, 큐를 사용해 비동기 코드를 안전하게 작성하는
방법을 배웠습니다. 다음 장에서는 자체 경제 시스템을 구축해 사용자에게 포인트와
가상 통화를 제공하는 기법을 살펴봅니다.