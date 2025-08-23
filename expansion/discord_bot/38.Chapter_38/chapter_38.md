# 38장 – 웹훅과 간단한 인터랙션

웹훅(webhook)은 봇을 사용하지 않고도 특정 채널에 메시지를 보낼 수 있는 간단한 방법입니다. 또한 다른 서비스에서 이벤트가 발생했을 때 디스코드 채널로 알림을 전송하는 데 자주 사용됩니다. `discord.Webhook` 클래스를 통해 메시지 전송, 임베드 첨부, 파일 업로드 등을 수행할 수 있습니다. 이 장에서는 웹훅을 생성하고 사용하는 방법을 설명합니다.

## 웹훅 생성과 사용

웹훅은 디스코드 클라이언트에서 채널 설정 → 통합 → 웹훅 메뉴에서 생성할 수 있습니다. 생성 후 URL을 복사하여 프로그램에서 사용할 수 있습니다. Python 코드에서 웹훅을 사용하려면 `discord.Webhook.from_url()` 메서드로 인스턴스를 생성합니다.

```python
import discord

WEBHOOK_URL = "https://discord.com/api/webhooks/..."
async def send_webhook():
    webhook = discord.Webhook.from_url(WEBHOOK_URL, session=None)
    await webhook.send(
        content="새로운 이벤트가 발생했습니다!",
        username="알림 봇",
        embed=discord.Embed(title="알림", description="서비스에서 새로운 이벤트가 감지되었습니다.")
    )
```

비동기 환경에서 `session` 인자로 `aiohttp.ClientSession`을 전달하여 연결을 재사용할 수 있습니다. 웹훅으로 보낸 메시지는 봇 메시지가 아니므로, 봇 계정의 이름과 아바타를 자유롭게 지정할 수 있습니다.

## 웹훅 관리

웹훅을 프로그래밍적으로 생성·삭제하거나 채널을 변경하려면 봇 권한이 필요합니다. `TextChannel.create_webhook()` 메서드로 새 웹훅을 만들고, `Webhook.delete()`로 제거할 수 있습니다. 또한 `Webhook.edit()`로 이름이나 아바타, 대상 채널을 수정할 수 있습니다.

## 슬래시 명령과 버튼을 통한 인터랙션

웹훅과 별개로, 디스코드 봇은 슬래시 명령과 버튼 등을 통해 사용자와 상호작용할 수 있습니다. 앞서 배운 `discord.ui.Button`과 `View`를 사용하면 동적으로 메시지를 업데이트하거나 새 메시지를 전송할 수 있습니다【716329102970593†L4889-L4924】.

## 요약

웹훅은 다른 서비스와 디스코드 채널을 쉽게 통합하는 방법을 제공합니다. 웹훅 URL을 안전하게 저장하고, 필요할 때만 사용할 수 있도록 관리하세요. 또한 봇의 인터랙션 기능과 결합하면 서버의 자동화된 알림 시스템을 구축할 수 있습니다.

