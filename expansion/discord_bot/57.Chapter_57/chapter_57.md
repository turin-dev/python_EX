# 캐싱과 샤딩 심화

대규모 서버나 많은 길드를 대상으로 하는 봇을 개발하면 **메모리 사용량**과 **지연 시간**이 중요한 이슈가 됩니다. `discord.py`는 기본적으로 대부분의 정보를 캐시에 저장하여 API 호출을 줄이지만, 필요에 따라 캐시를 줄이거나 샤딩을 통해 여러 프로세스로 분산할 수 있습니다.

## 캐시 관리

`Intents`를 통해 어떤 이벤트를 받을지 미리 결정함으로써 캐시에 저장되는 객체 수를 줄일 수 있습니다. 예를 들어, 멤버 정보를 캐시하지 않으려면 `intents.members`를 `False`로 설정하고, 메시지 내용을 다루지 않으면 `message_content` 인텐트를 끌 수 있습니다【666664033931420†L32-L45】. 또한 `discord.Client`의 `member_cache_flags` 속성을 조정해 **서버 멤버 캐시**를 끌 수 있습니다.

메시지 캐시의 크기는 `max_messages` 인수로 조절할 수 있습니다. 기본값은 1,000개이며, 메시지 캐시를 완전히 끄려면 `max_messages=None`으로 설정합니다. 캐시를 줄이면 메모리 사용량은 감소하지만, 수정/삭제 이벤트를 처리하기 위해 메시지를 다시 가져와야 할 수 있습니다.

```python
intents = discord.Intents(guilds=True, messages=True)
member_cache_flags = discord.MemberCacheFlags.none()  # 멤버 캐시 사용하지 않음
bot = commands.Bot(
    command_prefix="!",
    intents=intents,
    member_cache_flags=member_cache_flags,
    max_messages=100  # 최근 메시지 100개만 캐시
)
```

## 샤딩 개념과 구현

디스코드 게이트웨이는 한 연결에서 처리할 수 있는 서버 수에 제한이 있습니다. 봇이 많은 서버에 참여할 경우 **샤딩(sharding)**을 사용하여 여러 게이트웨이 연결로 부하를 분산해야 합니다. `discord.py`에서는 `AutoShardedBot`을 사용하면 자동으로 샤드를 생성하고 관리합니다. 샤드 수는 봇이 참여한 길드 수에 따라 결정되며, 봇에 할당된 `shard_count`를 초과하지 않아야 합니다.

```python
from discord.ext import commands

bot = commands.AutoShardedBot(command_prefix="!", intents=discord.Intents.all())

@bot.event
async def on_ready():
    print(f"Bot is ready. 샤드 수: {bot.shard_count}")

@bot.event
async def on_shard_ready(shard_id):
    print(f"Shard {shard_id} is ready")
```

샤딩을 사용하면 각 샤드가 별도의 웹소켓 연결을 유지하기 때문에 더 많은 서버를 효율적으로 처리할 수 있습니다. 그러나 샤드 간 데이터를 공유해야 할 때는 **데이터베이스나 메시지 브로커**를 통해 통신을 구현해야 합니다. 예를 들어 레벨 시스템이나 게임 상태를 여러 샤드에서 공유하는 경우 Redis 같은 중앙 저장소를 사용할 수 있습니다.

## 요약

캐시 설정과 샤딩을 적절히 조합하면 봇의 메모리 사용량을 제어하고 대규모 배포 환경에서 안정적으로 운영할 수 있습니다. 하지만 캐시를 너무 많이 줄이면 이벤트 처리 시 추가 API 호출이 발생하므로, 기능 요구사항에 맞춰 균형을 잡는 것이 중요합니다.

