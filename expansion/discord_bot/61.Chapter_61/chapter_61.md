# 웹훅을 이용한 서버 간 통신

웹훅(webhook)은 외부 애플리케이션이 디스코드 채널에 메시지를 보낼 수 있도록 하는 간단한 HTTP 엔드포인트입니다. 봇 내부에서도 웹훅을 사용하면 다른 서버나 채널로 익명 메시지를 전송하거나, 특정 이벤트를 외부 시스템에 전달할 수 있습니다. 이 장에서는 웹훅 생성과 메시지 전송, 그리고 재사용 전략을 살펴봅니다.

## 웹훅 생성 및 사용

길드의 텍스트 채널에는 여러 개의 웹훅을 생성할 수 있습니다. `discord.TextChannel.create_webhook()` 메서드를 사용해 봇이 직접 웹훅을 만들 수 있습니다. 웹훅에는 이름과 아바타를 지정할 수 있으며, 메시지를 전송할 때는 `webhook.send()`를 호출합니다. 다음 예제는 웹훅을 생성하고 다른 채널에서 재사용하는 방법을 보여줍니다:

```python
async def ensure_webhook(channel: discord.TextChannel, name: str) -> discord.Webhook:
    # 이미 동일 이름의 웹훅이 있는지 검색
    webhooks = await channel.webhooks()
    for hook in webhooks:
        if hook.name == name:
            return hook
    return await channel.create_webhook(name=name)

async def send_webhook_message(hook: discord.Webhook, content: str, username: str | None = None, avatar_url: str | None = None):
    await hook.send(content=content, username=username, avatar_url=avatar_url)
```

웹훅으로 전송된 메시지는 봇의 사용자명과 아바타가 아닌 지정된 값으로 표시됩니다. 따라서 알림용 봇, 공지 미러링 등에 적합합니다. 웹훅 URL은 노출되면 누구나 메시지를 보낼 수 있으므로, 비밀로 안전하게 관리해야 합니다.

## 교차 서버 알림 시스템

서버 A의 특정 채널에서 발생한 이벤트를 서버 B의 채널로 전달하려면 봇이 서버 B의 채널에 대해 미리 웹훅을 생성하고, 서버 A에서 이벤트를 감지하여 해당 웹훅을 통해 메시지를 전송하도록 구현합니다. 예를 들어 서버 A의 `#공지` 채널에 새로운 메시지가 올라오면 서버 B의 `#mirror` 채널로 복사할 수 있습니다:

```python
@bot.event
async def on_message(message: discord.Message):
    if message.guild.id == GUILD_A_ID and message.channel.id == ANNOUNCE_CHANNEL_ID:
        hook = await ensure_webhook(B_CHANNEL, "미러 공지")
        await send_webhook_message(
            hook,
            content=f"[{message.author.display_name}] {message.content}",
            avatar_url=message.author.display_avatar.url,
        )
```

이처럼 웹훅을 활용하면 서버 간 공지를 동기화하거나, 로그를 외부 저장소로 전송하는 등 다양한 통합 작업을 수행할 수 있습니다. 단, 웹훅 요청 횟수가 너무 많으면 레이트 리밋에 걸릴 수 있으므로 메시지를 버퍼링하거나 큐를 사용해 간격을 조정하는 것이 좋습니다.

## 요약

웹훅은 간단하지만 강력한 통신 도구입니다. 적절한 권한과 보안을 설정하여 서버 간 메시지 전달이나 외부 시스템과의 통합을 구현할 수 있습니다.

