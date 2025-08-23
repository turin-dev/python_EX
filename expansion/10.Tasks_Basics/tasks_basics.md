# 백그라운드 작업

봇이 정해진 간격으로 주기적인 작업을 수행해야 할 때 `discord.ext.tasks` 모듈을 이용하면 편리합니다. 예를 들어 일정 시간마다 서버 상태를 점검하거나, RSS 피드를 확인해 새로운 글을 알리는 등의 작업을 비동기적으로 실행할 수 있습니다. `@tasks.loop()` 데코레이터를 사용해 반복 실행 함수를 정의하고, `start()` 메서드를 호출하면 백그라운드에서 작업이 수행됩니다【230406618874054†L25-L36】.

## 1. loop 데코레이터 사용

기본적인 사용법은 다음과 같습니다. `seconds`, `minutes`, `hours` 중 하나를 지정하여 반복 간격을 설정할 수 있으며, `count` 파라미터를 사용하면 특정 횟수만큼 실행 후 자동 종료합니다:

```python
from discord.ext import tasks, commands

class MyCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.counter = 0

    @tasks.loop(seconds=5.0, count=10)
    async def printer(self):
        self.counter += 1
        print(f'{self.counter}번째 실행')

    @printer.before_loop
    async def before_printer(self):
        await self.bot.wait_until_ready()  # 봇이 준비될 때까지 대기

    @printer.after_loop
    async def after_printer(self):
        print('루프가 완료되었습니다.')

    def cog_unload(self):
        self.printer.cancel()  # 코그 언로드 시 루프 종료

def setup(bot):
    bot.add_cog(MyCog(bot))
    bot.get_cog('MyCog').printer.start()  # 루프 시작
```

위 예제에서 `@tasks.loop(seconds=5.0, count=10)`은 5초 간격으로 10회 반복하도록 설정합니다. `before_loop` 메서드는 루프 시작 전에 한 번만 실행되며, 여기서 `bot.wait_until_ready()`를 호출하여 클라이언트가 연결될 때까지 기다립니다【230406618874054†L122-L125】. `after_loop` 메서드는 루프가 종료된 후 한 번 실행되어 정리 작업을 할 수 있습니다【230406618874054†L87-L96】.

## 2. 시간 기반 스케줄링

`@tasks.loop` 데코레이터는 `time` 매개변수를 통해 하루 중 특정 시각에 실행되도록 설정할 수 있습니다. `datetime.time` 객체를 전달하거나 목록을 전달하여 하루에 여러 번 실행하도록 할 수 있습니다:

```python
import datetime as dt

@tasks.loop(time=dt.time(9, 0, 0))  # 매일 오전 9시 실행
async def morning_job():
    await some_channel.send('좋은 아침입니다!')

@tasks.loop(time=[dt.time(12, 0), dt.time(18, 0)])  # 정오와 오후 6시 두 번 실행
async def daily_reminder():
    await some_channel.send('점심 시간 또는 퇴근 시간입니다!')
```

`tasks.loop`는 내부적으로 다음 실행 시각까지 자동으로 대기하므로, 별도의 슬립을 구현할 필요가 없습니다. `timezone`을 지정하지 않으면 시스템 로컬 타임존을 사용합니다.

## 3. 루프 제어와 예외 처리

루프 객체는 실행 중 동적으로 간격을 변경할 수 있습니다. `change_interval(seconds=10.0)`과 같이 호출하면 다음 반복부터 새 간격이 적용됩니다. 또한, 루프 내부에서 예외가 발생하면 기본적으로 루프가 종료됩니다. 특정 예외만 무시하고 계속 실행하려면 `add_exception_type(ExceptionType)`을 사용합니다【230406618874054†L69-L74】.

```python
@my_loop.error
async def my_loop_error_handler(error):
    print(f'루프에서 오류 발생: {error!r}')

my_loop.add_exception_type(ConnectionError)  # 네트워크 오류가 발생해도 루프 계속
```

## 4. 단독 사용과 `discord.Client`

루프는 코그 클래스 외부에서도 사용할 수 있습니다. 클라이언트 또는 봇 객체를 사용하지 않는 간단한 스크립트에서도 다음과 같이 정의하여 사용할 수 있습니다:

```python
@tasks.loop(seconds=30)
async def heartbeat():
    print('30초마다 실행')

heartbeat.start()
```

단독 사용 시에도 `before_loop`나 `after_loop` 메서드를 정의하여 초기화와 정리 작업을 수행할 수 있습니다.

이 장에서는 백그라운드 작업을 주기적으로 실행하는 기본적인 방법을 살펴보았습니다. 다음 장에서는 작업을 더 세밀하게 제어하고 스케줄링하는 고급 기술을 학습합니다.



