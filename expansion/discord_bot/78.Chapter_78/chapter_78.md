# 여러 길드를 아우르는 기능 구현

하나의 봇이 여러 길드에 참여하면, 모든 길드에서 공통 데이터를 공유하거나
다른 길드에 메시지를 릴레이해야 하는 요구가 생깁니다. 이 장에서는 **글로벌
리더보드** 구현과 **메시지 브리지** 구축을 통해 여러 길드를 아우르는 봇을
만드는 방법을 소개합니다. 샤딩된 환경이라면 AutoShardedBot으로 각 샤드를
관리해야 하며【562972605132398†L2683-L2692】, 데이터 일관성을 위해 중앙 데이터베이스
또는 메시지 브로커를 사용해야 합니다.

## 글로벌 리더보드

포인트 시스템이 여러 서버에 걸쳐 있다면, 전체 사용자 중 상위권을 보여주는
리더보드를 만들 수 있습니다. 포인트를 저장하는 테이블에서 서버 ID를 추가로
저장하거나, 서버 구분 없이 전역적으로 합산할 수 있습니다. 예시 쿼리:

```sql
SELECT user_id, SUM(balance) AS total FROM balances GROUP BY user_id ORDER BY total DESC LIMIT 10;
```

이를 봇 명령으로 구현하면 다음과 같습니다.

```python
@commands.command(name="leaderboard")
async def leaderboard(ctx):
    rows = await db.fetch_all("SELECT user_id, SUM(balance) AS total FROM balances GROUP BY user_id ORDER BY total DESC LIMIT 10")
    description = "\n".join(f"<@{row['user_id']}>: {row['total']}" for row in rows)
    embed = discord.Embed(title="글로벌 리더보드", description=description)
    await ctx.send(embed=embed)
```

리더보드를 표시할 때는 멤버의 Display Name을 캐시하거나 Discord API로 `fetch_user`
하여 가져올 수 있습니다. 이름 조회가 느리기 때문에 캐싱 전략을 사용하면 응답
속도가 향상됩니다.

## 메시지 브리지 (Cross-Guild Relay)

특정 채널의 메시지를 다른 길드의 채널로 복제하는 **브릿지**를 구성하면
여러 서버 간 정보를 실시간으로 동기화할 수 있습니다. 예를 들어 공지사항을
모든 길드에 자동으로 보내거나, 하나의 게임 채팅을 여러 서버에서 공유하는
것이 가능합니다. 다음은 웹훅(Webhook)을 이용한 간단한 브리지 예제입니다.

```python
class BridgeCog(commands.Cog):
    def __init__(self, bot, source_channel_id: int, dest_channels: list[int]):
        self.bot = bot
        self.source = source_channel_id
        self.dest_channels = dest_channels
        self.webhooks: dict[int, discord.Webhook] = {}

    async def get_webhook(self, channel: discord.TextChannel) -> discord.Webhook:
        if channel.id in self.webhooks:
            return self.webhooks[channel.id]
        hooks = await channel.webhooks()
        if hooks:
            webhook = hooks[0]
        else:
            webhook = await channel.create_webhook(name="Relay")
        self.webhooks[channel.id] = webhook
        return webhook

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot or message.channel.id != self.source:
            return
        for dest_id in self.dest_channels:
            dest = self.bot.get_channel(dest_id)
            webhook = await self.get_webhook(dest)
            await webhook.send(
                content=message.content,
                username=message.author.display_name,
                avatar_url=message.author.display_avatar.url,
                allowed_mentions=discord.AllowedMentions.none(),
            )
```

브릿지는 메시지를 그대로 복제하기 때문에 멘션을 제거하거나 미디어 첨부를 처리하는
등 추가적인 로직이 필요합니다. 또한 권한 문제로 모든 길드에 웹훅 생성을
허용해야 합니다. 메시지를 수정/삭제하는 이벤트도 릴레이하려면 `on_message_edit`
과 `on_message_delete` 리스너를 구현해야 합니다.

## 전역 설정 관리

여러 길드에서 사용하는 봇의 설정(프리픽스, 포인트 지급률, 금지 단어 등)을
길드별로 저장하고 불러와야 할 때는 데이터베이스에 `guild_settings` 테이블을
만들어 `guild_id`를 키로 저장합니다. `commands.has_guild_permissions()`를
사용해 서버 관리자가 설정을 변경하도록 제한하고, 편집 UI는 슬래시 커맨드와
모달을 사용해 구현할 수 있습니다.

---

여러 길드를 지원하는 봇에서는 데이터와 이벤트를 일관성 있게 처리하는 것이
중요합니다. 다음 장에서는 맞춤형 도움말과 메뉴 시스템을 구축하여 사용자
경험을 향상시키는 방법을 배웁니다.