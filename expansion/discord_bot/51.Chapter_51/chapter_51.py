"""스케줄러와 타이머 예제.

이 모듈에는 길드 예약 이벤트를 생성하는 함수와
`discord.ext.tasks.loop`을 이용한 주기적인 공지 루프가 포함되어 있습니다.
실제 봇에서는 토큰과 채널 ID를 환경 변수로 관리하고, 필요한
길드 권한이 부여되어야 합니다.
"""

import datetime
import discord
from discord.ext import tasks, commands


async def schedule_study_event(bot: discord.Bot, guild_id: int, stage_channel_id: int) -> None:
    """주어진 길드와 스테이지 채널에서 1시간 뒤에 두 시간짜리 스터디 이벤트를 예약합니다.

    Parameters
    ----------
    bot: discord.Bot
        이벤트를 생성할 봇 인스턴스입니다.
    guild_id: int
        이벤트를 생성할 길드의 ID.
    stage_channel_id: int
        스테이지 채널의 ID.
    """
    guild = bot.get_guild(guild_id)
    if guild is None:
        raise ValueError("유효하지 않은 길드 ID")
    channel = guild.get_channel(stage_channel_id)
    if not isinstance(channel, discord.StageChannel):
        raise TypeError("지정한 채널이 스테이지 채널이 아닙니다")
    start = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=1)
    end = start + datetime.timedelta(hours=2)
    await guild.create_scheduled_event(
        name="Python 스터디",
        start_time=start,
        end_time=end,
        description="비동기 프로그래밍을 함께 공부합니다.",
        channel=channel,
        privacy_level=discord.PrivacyLevel.guild_only,
        type=discord.EntityType.stage_instance,
    )


class AnnouncementCog(commands.Cog):
    """매일 같은 시간에 공지를 보내는 예제 코그.

    봇이 준비되면 루프가 시작되며, 설정된 시간마다
    설정된 채널에 메시지를 전송합니다.
    """

    ANNOUNCEMENT_CHANNEL_ID: int

    def __init__(self, bot: commands.Bot, announcement_channel_id: int) -> None:
        self.bot = bot
        self.ANNOUNCEMENT_CHANNEL_ID = announcement_channel_id
        self.daily_announcement.start()

    @tasks.loop(time=datetime.time(hour=21, minute=0, tzinfo=datetime.timezone.utc))
    async def daily_announcement(self) -> None:
        channel = self.bot.get_channel(self.ANNOUNCEMENT_CHANNEL_ID)
        if channel and isinstance(channel, (discord.TextChannel, discord.Thread)):
            await channel.send("하루가 마무리됩니다. 내일도 화이팅!")

    @daily_announcement.before_loop
    async def before_daily(self) -> None:
        # 봇이 준비될 때까지 대기합니다.
        await self.bot.wait_until_ready()


# 봇을 설정할 때 위의 기능을 사용할 수 있습니다.
if __name__ == "__main__":
    intents = discord.Intents.default()
    intents.guilds = True
    # message_content intent는 루프 실행과 직접 관련은 없지만 테스트에 필요할 수 있습니다.
    intents.message_content = True
    bot = commands.Bot(command_prefix="!", intents=intents)

    @bot.event
    async def on_ready() -> None:
        print(f"Logged in as {bot.user}")
        # 코그 등록
        bot.add_cog(AnnouncementCog(bot, announcement_channel_id=123456789012345678))
        # 예제: 스터디 이벤트 예약
        # await schedule_study_event(bot, guild_id=YOUR_GUILD_ID, stage_channel_id=YOUR_STAGE_ID)

    # 실제 실행 시에는 토큰을 안전하게 가져오세요.
    # bot.run(os.getenv("DISCORD_TOKEN"))

