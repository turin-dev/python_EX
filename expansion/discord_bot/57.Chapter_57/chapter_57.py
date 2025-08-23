"""캐싱과 샤딩 설정 예제.

이 모듈은 봇의 캐시 정책을 조정하고 AutoShardedBot을 사용하는 간단한
설정 예제를 제공합니다. 실제 봇에서는 환경 변수로 토큰을 읽어 실행
합니다.
"""

import discord
from discord.ext import commands


def create_cached_bot() -> commands.Bot:
    """멤버 캐시를 비활성화하고 메시지 캐시 크기를 줄인 Bot을 생성합니다."""
    intents = discord.Intents(guilds=True, messages=True)
    member_cache_flags = discord.MemberCacheFlags.none()
    bot = commands.Bot(
        command_prefix="!",
        intents=intents,
        member_cache_flags=member_cache_flags,
        max_messages=100,
    )
    return bot


def create_sharded_bot() -> commands.AutoShardedBot:
    """자동 샤딩을 사용하는 Bot을 생성합니다."""
    intents = discord.Intents.all()
    bot = commands.AutoShardedBot(command_prefix="!", intents=intents)

    @bot.event
    async def on_ready() -> None:
        print(f"Login: {bot.user} | 샤드 수: {bot.shard_count}")

    @bot.event
    async def on_shard_ready(shard_id: int) -> None:
        print(f"Shard {shard_id} ready")

    return bot


if __name__ == "__main__":
    # 예제 실행: 캐시 최소화한 봇 인스턴스
    bot = create_cached_bot()
    # 또는 샤딩 봇을 사용하려면 다음 줄을 대신 사용하세요.
    # bot = create_sharded_bot()
    @bot.event
    async def on_ready() -> None:
        print("Bot ready")
    # bot.run(os.getenv("DISCORD_TOKEN"))

