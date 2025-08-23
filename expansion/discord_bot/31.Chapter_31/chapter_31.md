# 31장 – 작업 스케줄링 고급

앞서 `@tasks.loop` 데코레이터를 사용한 주기적 작업의 기본을 익혔다면, 이번 장에서는 더 다양한 스케줄링 옵션과 예외 처리 방법을 살펴봅니다. `discord.ext.tasks` 모듈은 시간을 지정해 하루에 여러 번 실행하거나, 특정 횟수만 실행하는 루프를 만들 수 있으며, 실행 간격을 동적으로 변경하는 기능도 제공합니다【230406618874054†L160-L210】.

## 시간 기반 스케줄링

루프를 하루에 한 번 이상 정해진 시간에 실행하려면 `time` 매개변수에 `datetime.time` 객체나 여러 객체를 전달합니다. 예를 들어 오전 9시와 오후 6시에 공지를 전송하는 루프는 다음과 같이 정의할 수 있습니다.

```python
from discord.ext import tasks
import datetime

@tasks.loop(time=[datetime.time(hour=9, minute=0), datetime.time(hour=18, minute=0)])
async def daily_announcements():
    # 서버의 일반 채널 ID를 지정하세요.
    channel = bot.get_channel(123456789012345678)
    await channel.send("하루 두 번의 공지입니다!")

@daily_announcements.before_loop
async def before_announcements():
    await bot.wait_until_ready()

```

시간 목록을 전달하면 루프가 지정된 시각마다 실행되며, 봇이 시작될 때 자동으로 다음 실행 시간을 계산합니다【230406618874054†L160-L210】.

## 반복 횟수와 인터벌 변경

`count` 인자를 사용하면 루프가 지정된 횟수만큼 실행된 후 자동으로 종료됩니다. 실행 중에 간격을 변경하려면 `change_interval()` 메서드를 호출합니다. 아래 예제는 5번 실행 후 루프를 종료하며, 마지막 실행에서 간격을 60초로 변경합니다.

```python
@tasks.loop(seconds=10, count=5)
async def limited_task():
    print(f"실행 번호: {limited_task.current_loop + 1}")
    if limited_task.current_loop == 3:
        limited_task.change_interval(seconds=60)

@limited_task.after_loop
async def after_limited_task():
    print("루프가 완료되었습니다!")
```

`limited_task.current_loop` 속성은 0부터 시작하는 실행 인덱스를 반환합니다. `after_loop` 데코레이터를 사용하면 루프가 종료된 뒤 후처리를 수행할 수 있습니다.

## 예외 처리

루프 실행 중 특정 예외를 무시하거나 다시 실행하려면 `add_exception_type()` 메서드에 예외 클래스를 등록합니다. 예를 들어 네트워크 오류가 발생해도 루프를 중단하지 않도록 할 수 있습니다【230406618874054†L25-L36】.

```python
@tasks.loop(seconds=30)
async def fetch_news():
    try:
        await fetch_latest_news()
    except NetworkError:
        pass  # 다음 루프에서 다시 시도

fetch_news.add_exception_type(NetworkError)
```

예외를 처리한 뒤에도 루프가 계속되며, 다른 예외는 기본적으로 종료됩니다.

## 요약

`discord.ext.tasks`는 루프의 실행 시각, 반복 횟수, 예외 처리, 실행 간격 변경 등 다양한 기능을 제공합니다. 이러한 옵션을 적절히 활용하여 봇의 반복 작업을 효율적으로 제어할 수 있습니다.

