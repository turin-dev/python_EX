# 작업 고급 기법

앞 장에서 소개한 기본 사용법을 넘어, `discord.ext.tasks.Loop` 객체는 다양한 파라미터와 메서드를 통해 작업 주기와 오류 처리, 동기화까지 세밀하게 제어할 수 있습니다. 이 장에서는 반복 횟수 제한, 정해진 시각 실행, 재연결 처리, 동기화 등 고급 기법을 다룹니다.

## 1. 반복 횟수와 종료 조건

`count` 매개변수는 루프가 실행될 총 횟수를 지정합니다. `None`(기본값)으로 설정하면 무한히 반복하고, 정수를 지정하면 지정한 횟수만큼 실행한 후 자동으로 `after_loop` 콜백을 호출하고 종료합니다. 예를 들어 이벤트 안내 메시지를 두 번만 보내고 싶다면:

```python
@tasks.loop(hours=1, count=2)
async def announce():
    await channel.send('이벤트가 곧 시작됩니다!')

@announce.after_loop
async def after():
    await channel.send('이벤트 안내가 종료되었습니다.')
```

루프를 코드에서 중지하려면 `loop.cancel()`을 호출합니다. 특정 조건에서 중지하려면 루프 내부에서 조건 체크 후 `self.loop.cancel()`을 호출할 수 있습니다.

## 2. 특정 시각에 실행

`time` 매개변수는 루프를 하루 중 한 번 또는 여러 번 지정된 시각에 실행하도록 합니다. `datetime.time` 객체 또는 `datetime.time` 객체 리스트를 전달하면, 각 시각에 루프가 실행됩니다. 예:

```python
@tasks.loop(time=[dt.time(8), dt.time(20)])
async def daily_greetings():
    await channel.send('좋은 하루 보내세요!')
```

이 경우 오전 8시와 오후 8시에 메시지를 전송합니다. `tasks.loop`는 다음 실행 시각까지 자동으로 대기하며, 어플리케이션을 재시작하면 현재 시각을 기준으로 다음 실행 시각을 계산합니다【230406618874054†L160-L210】.

## 3. 재연결 처리와 예외 무시

루프 실행 중 네트워크 오류나 특정 예외가 발생하면 루프가 종료될 수 있습니다. `Loop.add_exception_type(*exc_types)`를 호출하면 지정한 예외가 발생해도 루프가 종료되지 않고 무시됩니다【230406618874054†L69-L74】. 예를 들어, 일시적인 연결 문제를 무시하려면 `ConnectionError`를 추가합니다. 또한, `Loop.error()` 데코레이터로 오류 핸들러를 등록하면 예외 발생 시 사용자 정의 처리를 할 수 있습니다.

```python
@my_loop.error
async def my_loop_error(loop, error):
    # 로그 남기고 계속 진행
    print(f'루프 오류 발생: {error}')

my_loop.add_exception_type(ConnectionError, TimeoutError)
```

## 4. 동기화와 공유 상태

여러 루프나 명령어가 동시에 공유 자원(예: 리스트, 파일, 데이터베이스)을 수정하면 경쟁 조건이 발생할 수 있습니다. `asyncio.Lock` 같은 비동기 락을 사용하여 임계 영역을 보호하세요:

```python
class CounterCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.count = 0
        self.lock = asyncio.Lock()

    @tasks.loop(seconds=5)
    async def increment(self):
        async with self.lock:
            self.count += 1
            print(f'카운터: {self.count}')

    @commands.command()
    async def reset_count(self, ctx):
        async with self.lock:
            self.count = 0
            await ctx.send('카운터를 리셋했습니다.')
```

이처럼 락을 사용하면 루프와 명령어가 동시에 실행되어도 데이터 무결성을 유지할 수 있습니다.

## 5. 동적 간격 변경

루프가 실행되는 동안 `change_interval()` 메서드를 이용해 반복 주기를 변경할 수 있습니다. 예를 들어, 서버 부하에 따라 모니터링 주기를 조절하는 경우 다음과 같이 구현할 수 있습니다:

```python
@tasks.loop(seconds=30.0)
async def monitor():
    load = await get_server_load()
    # 부하가 높으면 간격을 10초로, 낮으면 60초로 변경
    if load > 0.8:
        monitor.change_interval(seconds=10.0)
    else:
        monitor.change_interval(seconds=60.0)
```

`change_interval`은 다음 반복부터 적용됩니다. 인터벌을 자주 변경하면 루프 스케줄러의 효율에 영향을 줄 수 있으므로 주의하세요.

이번 장에서는 백그라운드 루프의 고급 설정과 예외 처리, 동기화 기법을 다뤘습니다. 다음 장에서는 슬래시 커맨드를 시작으로 Discord 상호작용 시스템을 소개합니다.



