# 크론처럼 일정 예약하기

`discord.ext.tasks`의 루프는 간단한 간격 작업에 적합하지만, 매주 특정 요일/시간에 실행되는 작업을 설정하기에는 제한적입니다. 이를 위해 **APScheduler** 라이브러리를 사용하면 크론(cron) 표현식 또는 날짜 기반 트리거로 작업을 예약할 수 있습니다. 이 장에서는 APScheduler를 이용해 디스코드 봇과 함께 스케줄러를 실행하는 방법을 소개합니다.

## APScheduler 기본 사용법

APScheduler는 `pip install apscheduler` 명령으로 설치할 수 있습니다. `AsyncIOScheduler`를 사용하면 디스코드 봇과 동일한 이벤트 루프에서 작업을 실행할 수 있습니다. 다음 예제는 매일 오전 9시에 공지 채널에 인사 메시지를 보내는 작업을 등록합니다:

```python
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import datetime

async def daily_message():
    channel = bot.get_channel(ANNOUNCE_CHANNEL_ID)
    await channel.send("좋은 아침입니다! 오늘도 활기차게 시작하세요.")

scheduler = AsyncIOScheduler()
scheduler.add_job(daily_message, 'cron', hour=9, minute=0)
scheduler.start()
```

`cron` 트리거 외에도 `interval`(매 N초/분/시간)과 `date`(특정 시각)에 실행하는 트리거를 사용할 수 있습니다. 여러 작업을 동시에 등록할 수 있으며, 작업 ID를 지정해 나중에 취소하거나 수정할 수도 있습니다.

## 봇과 스케줄러 통합

APScheduler는 자체적으로 이벤트 루프를 생성하지 않으므로, 봇이 준비될 때 스케줄러를 시작해야 합니다. 보통 `on_ready` 이벤트에서 스케줄러를 초기화하는 것이 안전합니다:

```python
from discord.ext import commands
from apscheduler.schedulers.asyncio import AsyncIOScheduler

bot = commands.Bot(command_prefix="!")
scheduler = AsyncIOScheduler()

@bot.event
async def on_ready():
    print("Bot is ready")
    if not scheduler.running:
        scheduler.start()
    scheduler.add_job(daily_message, 'cron', hour=9, minute=0)
```

작업 함수는 비동기 함수여야 하며, 내부에서 `await`로 디스코드 API를 호출할 수 있습니다. 스케줄러를 중단하려면 `scheduler.shutdown()`을 호출합니다.

## 주의 사항

- APScheduler는 작업 실패에 대한 재시도 로직을 제공하지 않으므로, 작업 내부에서 예외를 처리하거나 `misfire_grace_time` 옵션을 지정해야 합니다.
- 크론 표현식은 서버 시간에 기반하므로, 타임존을 명시하거나 `timezone` 인자를 설정해 현지 시간에 맞추는 것이 좋습니다.

APScheduler를 이용하면 크론 스케줄링을 손쉽게 구현할 수 있어, 특정 요일·시간에 자동화 작업을 수행할 수 있습니다.

