# 스케줄러와 타이머

디스코드 봇을 운영하다 보면 특정 시점에 공지를 띄우거나 정기적으로 반복되는 작업을 실행해야 하는 경우가 많습니다. 이 장에서는 **길드 예약 이벤트(Guild Scheduled Events)** 기능과 봇 코드에서 타이머를 설정하는 방법을 살펴봅니다. 예약 이벤트는 서버 내에서 예정된 일정(예: 라이브 스트림, 스터디 모임)을 예고하고, 시간에 맞춰 알림을 보내는 기능입니다. 또한 `discord.ext.tasks` 모듈의 **루프(loop)** 데코레이터를 활용해 봇 내부에서 주기적으로 코드가 실행되도록 만들 수 있습니다.

## 길드 예약 이벤트 만들기

예약 이벤트는 음성 채널, 스테이지 채널, 외부 링크 등 다양한 형식으로 생성할 수 있습니다. 아래 예제는 스테이지 채널에서 Python 스터디 세션을 예약하는 코드입니다. 이벤트 생성에는 길드 관리 권한이 필요하며, `start_time`과 `end_time`은 `datetime` 객체로 전달합니다.

```python
import discord
from datetime import datetime, timezone, timedelta

async def schedule_study_event(bot: discord.Bot, guild_id: int, stage_channel_id: int):
    guild = bot.get_guild(guild_id)
    channel = guild.get_channel(stage_channel_id)
    start = datetime.now(timezone.utc) + timedelta(hours=1)
    end = start + timedelta(hours=2)
    await guild.create_scheduled_event(
        name="Python 스터디",
        start_time=start,
        end_time=end,
        description="비동기 프로그래밍을 함께 공부합니다.",
        channel=channel,
        privacy_level=discord.PrivacyLevel.guild_only,
        type=discord.EntityType.stage_instance
    )
```

이벤트는 생성 직후 길드의 이벤트 목록에 표시되며, 참여자들은 RSVP 버튼을 통해 알림을 받을 수 있습니다. 이벤트가 시작되면 스테이지 인스턴스가 자동으로 생성되고, 호스트는 청중을 스피커로 승격할 수 있습니다.

## 주기적인 작업과 타이머

길드 이벤트와 별개로, 봇 내부에서 정기적으로 실행되는 작업을 정의할 때는 `discord.ext.tasks.loop()` 데코레이터가 편리합니다. `loop` 데코레이터는 실행 간격을 초·분·시간 단위로 지정하거나, 특정 시각에 실행되도록 `time` 인자에 `datetime.time` 객체를 전달할 수 있습니다. 또한 `before_loop`와 `after_loop` 메서드를 사용하면 루프 시작 전후에 초기화나 정리 작업을 넣을 수 있습니다【230406618874054†L160-L210】.

다음 예제는 매일 오후 9시에 공지를 보내는 루프를 정의합니다. 루프는 봇이 준비되면 자동으로 시작되고, 서버 시간대에 맞춘 시계(`datetime.time(21, 0)`)를 사용합니다.

```python
from discord.ext import tasks
import datetime

class AnnouncementCog(discord.Cog):
    def __init__(self, bot: discord.Bot):
        self.bot = bot
        self.daily_announcement.start()

    @tasks.loop(time=datetime.time(hour=21, minute=0, tzinfo=datetime.timezone.utc))
    async def daily_announcement(self):
        channel = self.bot.get_channel(ANNOUNCEMENT_CHANNEL_ID)
        await channel.send("하루가 마무리됩니다. 내일도 화이팅!")

    @daily_announcement.before_loop
    async def before_daily(self):
        # 봇이 준비될 때까지 대기
        await self.bot.wait_until_ready()
```

루프는 `change_interval()` 메서드를 통해 실행 간격을 동적으로 변경할 수 있으며, `count` 매개변수를 사용하면 지정된 횟수만큼 실행하고 자동으로 종료하도록 만들 수도 있습니다【230406618874054†L160-L210】. 이러한 기능을 활용하면 일회성 타이머, 주기적인 데이터 백업, 이벤트 리마인더 등 다양한 시나리오를 손쉽게 구현할 수 있습니다.

## 정리

이 장에서는 디스코드 길드 예약 이벤트를 생성해 서버 차원에서 모임을 공지하는 방법과, `tasks.loop()`를 활용해 봇 내부에서 주기적인 작업을 수행하는 방법을 살펴보았습니다. 예약 이벤트를 활용하면 서버 구성원에게 일정을 미리 알릴 수 있고, 타이머를 통해 반복적으로 해야 하는 작업을 안정적으로 자동화할 수 있습니다.

\[타이머와 루프 기능 참조\]【230406618874054†L160-L210】

