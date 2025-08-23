# 인텐트 기본

**Gateway Intents**는 Discord 서버로부터 어떤 이벤트를 받을지 선언하는 필터이며, 봇의 권한을 세분화하여 최소 권한 원칙을 실천할 수 있도록 돕습니다. Intents를 설정하지 않으면 봇은 기본적인 시스템 이벤트만 수신하며, 메시지 내용이나 멤버 업데이트 같은 중요한 정보는 전달되지 않습니다【666664033931420†L32-L45】.

## 1. 기본 인텐트와 전체 인텐트

- `Intents.default()`: 대부분의 일반적인 이벤트(`guilds`, `messages`, `voice_states`, `reactions` 등)에 대한 구독을 포함하지만 민감한 정보(`members`, `presences`, `message_content`)는 제외합니다. 이 기본 설정은 많은 봇이 필요로 하는 최소한의 이벤트를 제공합니다.
- `Intents.all()`: Discord가 지원하는 모든 인텐트를 활성화합니다. 일부 인텐트는 *privileged*로 분류되어 있으며, 사용하려면 개발자 포털에서 별도로 활성화해야 합니다【666664033931420†L86-L114】.

개발할 봇의 기능에 따라 필요한 인텐트만 선택하여 권한을 최소화하는 것이 중요합니다. 예를 들어, 단순히 채팅 메시지를 읽고 응답하는 봇이라면 `message_content`와 `guilds`만으로도 충분할 수 있습니다.

## 2. 인텐트 설정 예제

`discord.Intents` 객체는 속성을 통해 필요한 이벤트를 선택적으로 켜고 끌 수 있습니다. 원하는 인텐트만 활성화하여 봇의 범위를 좁힐 수 있으며, 활성화하지 않은 인텐트에 대한 이벤트는 발생하지 않습니다. 아래 예제에서는 메시지와 길드 관련 이벤트만 구독합니다【666664033931420†L68-L83】:

```python
import discord

# 기본 인텐트를 가져오고 메시지와 길드만 활성화
intents = discord.Intents.none()  # 아무 이벤트도 구독하지 않음
intents.messages = True  # 메시지 이벤트 활성화
intents.guilds = True    # 길드 업데이트 이벤트 활성화

bot = discord.Bot(intents=intents)
```

또는 생성자에 직접 인자를 넘겨 줄 수도 있습니다:

```python
intents = discord.Intents(messages=True, guilds=True)
```

## 3. Privileged Intents

다음 인텐트는 **Privileged Intents**로 분류되어 있으며, 봇이 이 이벤트를 수신하려면 **개발자 포털**에서 설정을 활성화해야 합니다:

- `members`: 길드 멤버 목록과 가입/퇴장 이벤트를 수신합니다.
- `presences`: 멤버의 온라인 상태(접속, 활동 등)를 수신합니다.
- `message_content`: 메시지의 전체 내용을 수신합니다.

이 인텐트들은 개인 정보 보호 측면에서 제한되어 있으므로, 개발자 포털의 *Privileged Gateway Intents* 섹션에서 체크해야 합니다. 코드에서도 해당 속성을 `True`로 설정해야 합니다:

```python
intents = discord.Intents.default()
intents.members = True         # 멤버 목록 및 업데이트
intents.presences = True       # 멤버 상태 정보
intents.message_content = True # 메시지 내용
```

특히 **MESSAGE CONTENT INTENT**는 일반 봇 기능 중에서도 필수적인 경우가 많지만, 봇이 100개 이상의 서버에 참여할 때는 Discord의 승인이 필요합니다【666664033931420†L86-L114】.

## 4. Intents와 메모리 사용 고려

활성화하는 인텐트가 많아질수록 디스코드 게이트웨이에서 수신하는 이벤트의 양이 늘어나고 메모리 사용량이 증가합니다. 불필요한 인텐트를 끄면 네트워크 트래픽과 메모리 사용을 줄일 수 있습니다. 예를 들어, 멤버 상태나 게임 활동을 이용하지 않는 봇이라면 `presences` 인텐트를 비활성화해도 무방합니다. 필요한 정보만 수신하도록 설계하는 것이 봇 성능과 안정성에 도움이 됩니다.

이 장에서는 Intents의 기본 개념과 설정 방법을 소개했습니다. 다음 장에서는 명령어 시스템을 제공하는 `commands.Bot` 클래스를 사용해 봇 명령을 구현하는 방법을 알아봅니다.



