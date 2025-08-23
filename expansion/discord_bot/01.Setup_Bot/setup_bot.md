# 디스코드 봇 설정

이 장에서는 Discord 개발자 포털에서 새 애플리케이션을 만들고, 봇을 생성하여 토큰을 발급받는 과정을 단계별로 안내합니다. 디스코드 봇은 일반 봇 계정과 달리 개발자가 직접 생성하고 관리해야 하므로, **Discord 개발자 계정**이 있어야 합니다. 또한 `discord.py` 라이브러리는 비동기 라이브러리이기 때문에 Python 3.8 이상 버전이 필요하며, 봇 코드는 항상 `async`/`await` 문법을 사용해야 합니다.

## 1. 개발자 포털에서 애플리케이션 생성

1. [Discord Developer Portal](https://discord.com/developers/applications)에 접속하여 로그인합니다.
2. **New Application** 버튼을 클릭하고 봇의 이름을 지정합니다. 애플리케이션 생성 후 좌측 메뉴에서 **Bot** 섹션을 선택해 **Add Bot**을 클릭하여 봇 계정을 생성합니다. 이때 봇의 **username**과 **avatar**를 지정할 수 있습니다.
3. 봇을 만들면 **TOKEN**을 확인할 수 있습니다. 토큰은 봇과 Discord 서버 간의 인증에 사용되는 비밀 문자열로, 제3자가 토큰을 획득하면 봇을 임의로 제어할 수 있으므로 절대 외부에 노출하지 말아야 합니다. 토큰은 환경 변수나 `.env` 파일에 저장하고 코드에서는 `os.getenv('DISCORD_TOKEN')`처럼 불러오는 방식이 권장됩니다.

## 2. 권한과 OAuth2 URL 설정

봇을 서버에 초대하기 위해서는 적절한 권한을 설정한 OAuth2 URL을 생성해야 합니다. **OAuth2 → URL Generator** 메뉴에서 **SCOPES** 항목에서 `bot`을 선택하고, **BOT PERMISSIONS**에서는 봇이 수행할 기능에 따라 권한을 선택합니다. 기본적으로는 메시지를 읽고 보내는 권한이 필요하며, 관리 명령을 구현하려면 `Manage Roles`, `Kick Members` 등 추가 권한을 선택합니다. 생성된 URL을 브라우저 주소창에 입력하면 봇을 초대할 수 있는 서버 목록이 나타납니다.

## 3. Intents 활성화

Discord API 1.5부터는 **Gateway Intents**를 통해 봇이 어떤 이벤트를 수신할지 명시적으로 선언해야 합니다【666664033931420†L32-L45】. 예를 들어 채팅 메시지를 수신하려면 **MESSAGE CONTENT INTENT**를 활성화해야 합니다. 개발자 포털의 **Bot** 설정 페이지에서 *Privileged Gateway Intents* 옵션 중 필요한 항목(예: `MESSAGE_CONTENT INTENT`, `PRESENCE INTENT`, `MEMBERS INTENT`)을 활성화합니다. 코드를 작성할 때도 다음과 같이 `discord.Intents` 객체를 전달해야 합니다:

```python
import os
import discord

intents = discord.Intents.default()
intents.message_content = True  # 메시지 콘텐츠 접근 권한 활성화

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"봇 로그인: {client.user}")

client.run(os.getenv("DISCORD_TOKEN"))
```

이처럼 Intents를 설정하지 않으면 Discord가 봇에게 메시지 내용이나 멤버 목록을 전달하지 않으므로, 코드를 작성할 때 항상 필요한 Intents를 활성화해야 합니다. 민감한 Intents(`MESSAGE_CONTENT`, `PRESENCES`, `MEMBERS`)는 개발자 포털에서 별도로 승인을 받아야 하며, 봇이 100개 이상의 서버에 참가한 경우에는 Discord에 추가 검토를 요청해야 합니다【666664033931420†L86-L114】.

## 4. 보안과 관리 팁

- **토큰 보호**: 토큰을 깃허브 등의 공개 저장소에 커밋하지 않도록 주의하세요. `.gitignore`에 `.env` 파일을 추가하고 토큰을 환경 변수로 관리합니다.
- **개발과 테스트 분리**: 실제 서비스용 봇과 개발용 봇을 별도로 생성하여 테스트 환경에서 마음껏 실험하세요.
- **비동기 프로그래밍**: `discord.py`는 asyncio 기반으로 동작합니다. 블로킹 작업(예: 파일 입출력, 네트워크 요청)은 `asyncio.to_thread()`나 비동기 라이브러리를 사용해 실행하여 이벤트 루프가 멈추지 않게 합니다.

이 장에서는 디스코드 봇 생성의 전체적인 흐름과 초기 설정을 정리했습니다. 다음 장에서는 Python 환경 설정과 `discord.py` 설치 과정을 자세히 살펴보겠습니다.



