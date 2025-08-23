"""
샤딩과 교차 샤드 통신 예제.

이 스크립트는 `discord.ext.commands.AutoShardedBot`을 사용해 자동 샤딩
봇을 생성하는 방법과 Redis를 통해 샤드 간 브로드캐스트를 구현하는 예를
보여줍니다. 실제 배포에서는 환경 변수로 토큰과 Redis URL을 주입해야
하며, Redis 서버가 실행되고 있어야 합니다.

주의: 이 코드는 샤딩 환경과 Redis 설정이 갖춰진 곳에서만 제대로 동작합니다.
봇을 테스트할 때는 한두 개의 샤드만 사용하거나 `commands.Bot`으로 충분합니다.
"""

import asyncio
import os
import discord
from discord.ext import commands, tasks

try:
    import aioredis  # 선택 사항: Redis가 없는 환경에선 임포트 오류
except ImportError:
    aioredis = None  # redis 라이브러리가 없으면 None


class ShardedBot(commands.AutoShardedBot):
    """자동 샤딩 봇.

    초기화 시 on_ready 이벤트에서 샤드 정보를 출력하고, Redis 구독을 시작합니다.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Redis 구독 태스크 핸들러
        self.redis_task: asyncio.Task | None = None

    async def setup_hook(self) -> None:
        # 첫 샤드에서만 글로벌 초기화를 수행
        if self.shard_id == 0:
            print("ShardedBot setup_hook on shard 0: performing global setup")
            # 예: 데이터베이스 연결 초기화 등

    async def on_ready(self) -> None:
        print(f"Logged in as {self.user} (Shard {self.shard_id}/{self.shard_count})")
        # Redis 리스너 태스크를 시작
        if aioredis and not self.redis_task:
            self.redis_task = asyncio.create_task(self.redis_listener())

    async def redis_listener(self) -> None:
        """
        Redis Pub/Sub 리스너.

        모든 샤드는 'broadcast' 채널을 구독하고, 메시지를 수신하면 지정한
        작업을 수행합니다. 예를 들어 "refresh_cache" 메시지를 받으면
        캐시를 갱신합니다.
        """
        redis_url = os.getenv("REDIS_URL", "redis://localhost")
        redis = aioredis.from_url(redis_url)
        pubsub = redis.pubsub()
        await pubsub.subscribe("broadcast")
        try:
            async for message in pubsub.listen():
                if message.get("type") != "message":
                    continue
                payload = message["data"].decode()
                print(f"Shard {self.shard_id} received broadcast: {payload}")
                if payload == "refresh_cache":
                    await self.refresh_cache_global()
        finally:
            await pubsub.close()

    async def refresh_cache_global(self) -> None:
        """샤드 로컬 캐시를 갱신하는 예제 메서드."""
        # 실제 구현에서는 데이터베이스에서 정보를 다시 로드
        print(f"Shard {self.shard_id}: refreshing cache")


async def broadcast_refresh() -> None:
    """모든 샤드에 캐시 갱신 요청을 브로드캐스트하는 함수."""
    if not aioredis:
        raise RuntimeError("aioredis가 설치되어 있지 않습니다. pip install aioredis")
    redis_url = os.getenv("REDIS_URL", "redis://localhost")
    redis = aioredis.from_url(redis_url)
    await redis.publish("broadcast", "refresh_cache")
    await redis.close()


def main() -> None:
    intents = discord.Intents.default()
    # 필요하다면 Privileged Intents 설정
    bot = ShardedBot(command_prefix="!", intents=intents)

    # 단순 테스트 명령: 모든 샤드에서 핑 메시지를 전송
    @bot.command()
    async def ping(ctx: commands.Context) -> None:
        await ctx.send(f"Pong from shard {bot.shard_id}!")

    # 캐시 갱신 명령: 채팅 명령으로 다른 샤드에 갱신 요청
    @bot.command()
    async def refresh(ctx: commands.Context) -> None:
        await broadcast_refresh()
        await ctx.send("모든 샤드에 캐시 갱신 신호를 전송했습니다.")

    bot.run(os.getenv("DISCORD_TOKEN"))


if __name__ == "__main__":
    main()