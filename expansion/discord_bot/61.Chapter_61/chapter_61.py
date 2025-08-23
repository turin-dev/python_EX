"""웹훅을 이용한 서버 간 통신 예제.

이 모듈은 텍스트 채널에 웹훅을 생성하거나 검색하고, 해당 웹훅을 통해
메시지를 전송하는 함수를 제공합니다. 교차 서버 알림 시스템 등에서
재사용할 수 있습니다.
"""

import discord


async def ensure_webhook(channel: discord.TextChannel, name: str) -> discord.Webhook:
    """채널에 동일 이름의 웹훅이 있으면 반환하고, 없으면 새로 생성합니다."""
    hooks = await channel.webhooks()
    for hook in hooks:
        if hook.name == name:
            return hook
    return await channel.create_webhook(name=name)


async def send_webhook_message(
    hook: discord.Webhook,
    content: str,
    username: str | None = None,
    avatar_url: str | None = None,
) -> None:
    """웹훅을 통해 메시지를 전송합니다."""
    await hook.send(content=content, username=username, avatar_url=avatar_url)


# 예제 사용:
# hook = await ensure_webhook(channel, "공지 미러")
# await send_webhook_message(hook, content="안녕하세요!", username="Mirror", avatar_url=None)

