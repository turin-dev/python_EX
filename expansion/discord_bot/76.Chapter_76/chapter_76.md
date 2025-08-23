# 외부 API 통합하기: 날씨, 번역, 기타 서비스

디스코드 봇은 외부 서비스를 호출하여 날씨 정보를 제공하거나, 텍스트를 번역하거나,
위키백과 검색 결과를 반환하는 등 다양한 기능을 수행할 수 있습니다. 이 장에서는
비동기 HTTP 라이브러리(`aiohttp`)를 사용해 RESTful API를 호출하는 방법과,
API 키를 안전하게 관리하는 방법, 응답을 적절히 캐싱하고 오류를 처리하는
패턴을 소개합니다. 외부 API 호출은 속도 제한이 있으므로 세마포어를 사용해
동시에 호출하는 횟수를 제한합니다【230406618874054†L160-L210】.

## 비동기 HTTP 클라이언트 사용

`aiohttp`는 asyncio 기반의 HTTP 클라이언트로, `async with` 문맥에서 세션을
관리할 수 있습니다. 세션을 재사용하면 TCP 커넥션 재사용을 통해 효율을 높일
수 있습니다. 예를 들어 OpenWeatherMap API를 호출해 현재 날씨를 가져오는
함수는 다음과 같습니다.

```python
import os
import aiohttp

API_KEY = os.getenv("OPENWEATHER_API_KEY")

async def fetch_weather(city: str) -> str:
    params = {"q": city, "appid": API_KEY, "units": "metric", "lang": "kr"}
    async with aiohttp.ClientSession() as session:
        async with session.get("https://api.openweathermap.org/data/2.5/weather", params=params) as resp:
            if resp.status != 200:
                return "날씨 정보를 가져오지 못했습니다."
            data = await resp.json()
    desc = data["weather"][0]["description"]
    temp = data["main"]["temp"]
    return f"{city}의 현재 날씨: {desc}, {temp:.1f}°C"
```

## 번역 API 호출

다양한 무료 번역 API가 존재합니다. 여기서는 MyMemory 번역 API를 사용해
간단한 번역 봇을 만들어 봅니다. 쿼리 문자열에 원문과 타겟 언어 코드를 지정하면
JSON 형태의 번역 결과를 받을 수 있습니다.

```python
async def translate_text(text: str, target_lang: str = "en") -> str:
    async with aiohttp.ClientSession() as session:
        async with session.get(
            "https://api.mymemory.translated.net/get",
            params={"q": text, "langpair": f"auto|{target_lang}"},
        ) as resp:
            data = await resp.json()
    return data["responseData"]["translatedText"]
```

## 캐싱과 오류 처리

외부 API는 요청 횟수에 제한이 있으므로 동일한 요청을 반복하면 응답을 캐시해야
합니다. 간단한 캐싱은 딕셔너리나 LRU 캐시로 구현할 수 있으며, 라이브러리
`functools.lru_cache`를 사용할 수도 있습니다. 또한 네트워크 오류나 API의 오류
응답에 대비해 예외 처리를 해야 합니다.

```python
from functools import lru_cache

@lru_cache(maxsize=128)
async def cached_weather(city: str) -> str:
    try:
        return await fetch_weather(city)
    except Exception as e:
        return f"날씨 API 오류: {e}"
```

## Discord 명령으로 통합

이제 위의 함수를 Cog에 통합하여 명령어로 제공해 보겠습니다. 세마포어를
사용해 동시에 3개만 호출하도록 제한하고, 명령 실행 시 입력을 검증합니다.

```python
class IntegrationCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.sem = asyncio.Semaphore(3)

    @commands.command(name="날씨")
    async def weather_cmd(self, ctx, *, city: str):
        async with self.sem:
            result = await fetch_weather(city)
        await ctx.send(result)

    @commands.command(name="번역")
    async def translate_cmd(self, ctx, target_lang: str, *, text: str):
        async with self.sem:
            translation = await translate_text(text, target_lang)
        await ctx.send(f"{target_lang} 번역: {translation}")
```

API 키는 코드에 하드코딩하지 말고 `.env` 파일이나 서버의 환경 변수로 관리하세요.
에러 메시지를 사용자에게 그대로 노출하지 말고, 관리자에게만 구체적인 오류를
로그로 남기도록 합니다.

---

외부 API 통합은 봇의 기능을 무한히 확장시킬 수 있지만, 속도 제한과 오류 처리,
보안에 특히 신경을 써야 합니다. 다음 장에서는 리치 메시지와 임베드 디자인을
세련되게 만드는 방법을 알아봅니다.