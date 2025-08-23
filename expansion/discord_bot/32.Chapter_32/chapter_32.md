# 32장 – HTTP 통합과 외부 API 호출

봇이 외부 서비스와 상호 작용할 수 있도록 HTTP 요청을 보내는 기능은 매우 중요합니다. 예를 들어 날씨 정보를 가져오거나 뉴스 헤드라인을 전송하려면 REST API를 호출해야 합니다. 파이썬에서는 `aiohttp` 라이브러리가 비동기 HTTP 클라이언트를 제공하여 Discord 봇과 잘 어울립니다.

## aiohttp로 GET 요청 보내기

`aiohttp.ClientSession`은 세션을 재사용하여 연결 성능을 개선합니다. 다음 예제는 공개 API에서 JSON 데이터를 가져와 간단히 파싱하는 방법을 보여 줍니다.

```python
import aiohttp
import discord
from discord.ext import commands

bot = commands.Bot(command_prefix="!")

@bot.command()
async def 현재날씨(ctx, city: str):
    async with aiohttp.ClientSession() as session:
        async with session.get(f"https://wttr.in/{city}?format=j1") as resp:
            if resp.status != 200:
                await ctx.send("날씨 정보를 가져오는 데 실패했습니다.")
                return
            data = await resp.json()
    temp_c = data["current_condition"][0]["temp_C"]
    await ctx.send(f"{city}의 현재 기온은 {temp_c}°C 입니다.")
```

`session.get()` 호출에서 응답 상태를 확인한 뒤 `resp.json()`으로 JSON 데이터를 파싱합니다. 네트워크 요청은 예외가 발생할 수 있으므로 `try`/`except`를 사용해 오류를 처리하고, 오래 걸리는 요청은 타임아웃을 지정하는 것이 좋습니다.

## POST 요청과 헤더 설정

API에 데이터를 제출해야 할 때는 `session.post()`를 사용하며, `json=`이나 `data=` 인자로 본문을 전달합니다. 또한 `headers` 매개변수로 인증 토큰이나 콘텐츠 타입을 설정할 수 있습니다.

```python
async def create_ticket(user_id: int, description: str) -> int:
    payload = {"user": user_id, "desc": description}
    headers = {"Authorization": "Bearer YOUR_API_KEY"}
    async with aiohttp.ClientSession() as session:
        async with session.post("https://api.example.com/tickets", json=payload, headers=headers) as resp:
            resp.raise_for_status()
            result = await resp.json()
    return result["ticket_id"]
```

`resp.raise_for_status()`는 응답 코드가 오류일 경우 예외를 발생시켜 호출자가 적절히 처리할 수 있게 합니다.

## 세션 재사용과 종료

여러 명령어에서 HTTP 요청을 반복적으로 수행하면 매번 새 세션을 생성하는 대신 하나의 세션을 재사용하는 것이 효율적입니다. 봇 시작 시 세션을 생성해 `bot.http_session`과 같은 속성에 저장하고, 종료 시 `close()`를 호출합니다. `discord.Client.close()`를 오버라이드하여 세션을 함께 닫는 것도 좋은 방법입니다.

## 요약

외부 API와 통합할 때는 `aiohttp`를 사용해 비동기로 요청을 보내고 응답을 처리합니다. 오류 처리를 철저히 하여 사용자에게 적절한 메시지를 전달하고, 세션을 재사용해 성능을 개선하세요. 필요하다면 레이트 리밋과 타임아웃을 설정해 서비스 안정성을 높일 수 있습니다【230406618874054†L25-L36】.

