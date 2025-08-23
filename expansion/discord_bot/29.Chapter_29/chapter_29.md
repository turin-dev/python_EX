# 29장 – 캐시 전략과 샤딩(Sharding)

대규모 봇은 여러 길드와 채널에 연결되기 때문에 메모리 사용량과 API 호출 수를 최적화해야 합니다. `discord.py`는 이벤트 처리 속도를 향상시키기 위해 대부분의 객체를 메모리에 **캐시** 합니다. 그러나 캐시가 너무 커지면 메모리를 과도하게 사용하게 되므로, 필요한 데이터만 캐싱하거나 불필요한 데이터는 비활성화할 수 있습니다. 또한 많은 서버를 관리하려면 샤딩을 통해 여러 프로세스에 부하를 분산할 수 있습니다.

## 캐시 크기 조절

`discord.Client`와 `commands.Bot`에는 `max_messages` 매개변수가 있어 메시지 캐시 크기를 조절할 수 있습니다. 기본값은 1,000개이며, `None`으로 설정하면 모든 메시지를 캐시합니다. 캐시 크기를 줄이면 메모리 사용량을 줄일 수 있지만, `on_message_edit` 같은 이벤트의 정보가 캐시에 존재하지 않아 일부 기능이 제한될 수 있습니다【549557713116431†L69-L76】.

```python
bot = commands.Bot(command_prefix="!", max_messages=100)
```

특정 데이터만 캐싱하려면 Intents를 조절해 멤버 목록이나 프리센스 정보를 수신하지 않도록 설정할 수 있습니다. 예를 들어 멤버 정보를 사용하지 않는다면 `intents.members = False`로 설정해 캐시를 줄입니다.

## 샤딩으로 확장하기

**샤딩(Sharding)** 은 봇이 여러 게이트웨이 연결을 동시에 사용하여 Discord의 부하를 분산하는 기술입니다. `AutoShardedBot`을 사용하면 shard 수를 자동으로 계산하여 인스턴스를 여러 개로 나누어 실행할 수 있습니다.

```python
from discord.ext import commands

bot = commands.AutoShardedBot(command_prefix="!", intents=discord.Intents.default())

@bot.event
async def on_ready():
    print(f"봇이 준비되었습니다. 샤드 수: {bot.shard_count}")
```

샤딩된 봇은 `bot.get_guild(guild_id)`를 호출할 때 올바른 shard에서 데이터를 가져와야 하며, shard 간 통신을 위해 브로드캐스트 메커니즘을 구현할 필요가 있습니다. 예를 들어 Redis나 데이터베이스를 통해 공통 데이터를 공유하거나, 내부 IPC(Inter-Process Communication) 라이브러리를 사용해 shard 간 명령을 전달할 수 있습니다.

## 요약

성능과 확장성을 위해 캐시 크기와 Intents를 신중하게 조절하고, 필요한 경우 샤딩을 도입하여 부하를 분산하세요. 캐시를 줄이면 메모리를 절약할 수 있지만 일부 이벤트가 작동하지 않을 수 있으므로 트레이드오프를 이해해야 합니다. 샤딩을 사용할 때는 shard 간 데이터 동기화 방법을 마련해 전체 봇 상태를 유지하십시오.

