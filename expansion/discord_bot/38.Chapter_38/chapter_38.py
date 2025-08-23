"""웹훅 사용 예제.

웹훅 URL을 이용해 채널에 메시지와 임베드를 전송하는 방법을 보여 줍니다.
"""

import asyncio
import discord


# 생성된 웹훅 URL을 여기에 입력하세요.
WEBHOOK_URL = "https://discord.com/api/webhooks/your_id/your_token"


async def send_webhook_message() -> None:
    """웹훅을 통해 메시지를 전송합니다."""
    webhook = discord.Webhook.from_url(WEBHOOK_URL, session=None)
    embed = discord.Embed(title="알림", description="서비스에서 새로운 이벤트가 감지되었습니다.")
    await webhook.send(
        content="새로운 이벤트가 발생했습니다!",
        username="알림 봇",
        embed=embed,
    )


if __name__ == "__main__":
    asyncio.run(send_webhook_message())