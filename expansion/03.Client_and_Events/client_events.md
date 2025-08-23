# 클라이언트와 기본 이벤트

디스코드 봇은 `discord.Client` 또는 `discord.ext.commands.Bot` 객체를 통해 Discord 게이트웨이에 연결합니다. 이 장에서는 저수준 클라이언트(`Client`)를 사용하여 이벤트 기반 프로그래밍을 이해하고, 주요 이벤트 핸들러를 구현하는 방법을 설명합니다. 이후 장에서 봇 명령어 시스템을 사용할 때에는 `Bot` 클래스를 사용할 것이지만, `Client`를 이해하면 이벤트 흐름과 비동기 처리에 익숙해질 수 있습니다.

## 1. 클라이언트 생성과 Intents 설정

`discord.Client`는 Discord 서버와 WebSocket 연결을 유지하고, 봇이 수신하는 이벤트를 처리합니다. Intents는 클라이언트가 어떤 이벤트를 수신할지 결정하는 필터이며, 클라이언트 인스턴스를 생성할 때 `intents` 매개변수로 전달해야 합니다【666664033931420†L32-L45】. 예를 들어 메시지 수신과 길드 멤버 정보를 사용하려면 다음과 같이 설정합니다:

```python
import os
import discord

intents = discord.Intents.default()
intents.message_content = True    # 메시지 내용 접근 허용
intents.members = True            # 길드 멤버 업데이트 수신

client = discord.Client(intents=intents)
```

Intents를 설정하지 않으면 디스코드 API는 기본 이벤트만 전송하며, 메시지 내용 등 중요한 정보가 누락될 수 있습니다. 특히 `message_content` intents는 봇이 메시지를 읽을 수 있도록 해주므로, 일반 메시지를 처리하는 봇에서는 필수입니다【666664033931420†L86-L114】.

## 2. 이벤트 핸들러 구현

클라이언트는 다양한 이벤트를 `@client.event` 데코레이터를 사용하여 처리할 수 있습니다. 이벤트 핸들러는 항상 `async def`로 정의되어야 하며, Discord가 해당 이벤트를 발생시키면 자동으로 호출됩니다.

### `on_ready`

봇이 Discord 게이트웨이에 연결을 완료하면 `on_ready` 이벤트가 호출됩니다. 이 이벤트에서 봇의 초기화 작업을 수행할 수 있습니다. 예를 들면, 봇이 로그인한 사용자 이름과 ID를 출력하는 코드입니다:

```python
@client.event
async def on_ready():
    print(f"{client.user} 로 준비 완료. 사용 가능 길드 수: {len(client.guilds)}")
```

### `on_message`

채널에 새 메시지가 도착하면 `on_message` 이벤트가 발생합니다. 이 핸들러를 이용해 특정 단어에 반응하거나 명령어 시스템을 직접 구현할 수 있습니다. 예를 들어, 사용자가 "ping"을 입력하면 "pong"으로 응답하는 봇을 만들어 보겠습니다:

```python
@client.event
async def on_message(message: discord.Message):
    # 봇 자신의 메시지는 무시
    if message.author == client.user:
        return

    if message.content.lower() == 'ping':
        await message.channel.send('pong')

    # 멘션으로 인사하기
    if '안녕' in message.content:
        await message.channel.send(f'{message.author.mention}님, 안녕하세요!')
```

`on_message` 이벤트를 사용할 때는 **명령어 프리픽스와 구분하는 로직**을 직접 작성해야 합니다. 이후 장에서 소개하는 `commands.Bot`을 사용하면 이러한 명령어 파싱을 자동으로 처리할 수 있습니다.

### 기타 주요 이벤트

- `on_member_join(member)`: 새 멤버가 서버에 가입했을 때 호출되며, 환영 메시지를 보내거나 역할을 자동 부여하는 데 사용합니다.
- `on_member_remove(member)`: 멤버가 서버를 떠났을 때 호출됩니다.
- `on_error(event, *args, **kwargs)`: 이벤트 핸들러에서 예외가 발생했을 때 호출되어 예외 처리 및 로깅을 할 수 있습니다.
- `on_reaction_add(reaction, user)`: 사용자가 이모지를 추가했을 때 호출되며, 리액션 역할 부여 등에 활용할 수 있습니다.

각 이벤트의 시그니처와 동작 방식은 공식 문서에서 확인할 수 있으며, 필요한 Intents가 활성화되어 있어야 이벤트가 정상적으로 호출됩니다.

## 3. 클라이언트 실행

이벤트 핸들러를 정의한 후에는 `client.run(TOKEN)`을 호출하여 봇을 실행합니다. 이 함수는 내부에서 비동기 이벤트 루프를 생성하고 Discord 서버와 연결합니다. 앞서 언급했듯이 토큰은 안전하게 저장된 환경 변수에서 불러오는 것이 좋습니다. `client.run()` 호출 이후에는 코드가 블로킹되므로, 봇 실행 중 다른 작업을 수행하려면 별도 스레드나 프로세스를 사용해야 합니다.

```python
if __name__ == '__main__':
    client.run(os.getenv('DISCORD_TOKEN'))
```

이 장에서는 기본 클라이언트와 이벤트 처리 흐름을 설명했습니다. 다음 장에서는 Intents의 종류와 용도를 보다 자세히 알아보고, `commands.Bot`을 사용한 명령어 시스템을 구축해 보겠습니다.



