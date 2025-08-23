# 웹 대시보드와 API 통합

봇의 설정을 웹 인터페이스에서 관리하거나, 다른 서비스와 통신하는 API를 제공하려면 HTTP 서버를 함께 실행해야 합니다. `discord.py`는 자체적으로 웹 서버 기능을 제공하지 않지만, `aiohttp`나 `FastAPI` 같은 비동기 웹 프레임워크를 사용하면 봇과 같은 이벤트 루프에서 HTTP 요청을 처리할 수 있습니다.

## aiohttp를 이용한 간단한 대시보드

`aiohttp.web` 모듈을 사용하면 경량 웹 서버를 쉽게 구축할 수 있습니다. 다음 예제는 봇과 함께 실행되는 간단한 웹 서버를 생성하고, `/status` 엔드포인트에서 봇의 온라인 상태와 길드 수를 반환합니다.

```python
from aiohttp import web
import discord
from discord.ext import commands

bot = commands.Bot(command_prefix="!", intents=discord.Intents.default())

async def status_handler(request: web.Request) -> web.Response:
    return web.json_response({
        "online": bot.is_ready(),
        "guild_count": len(bot.guilds),
    })

def create_web_app() -> web.Application:
    app = web.Application()
    app.add_routes([web.get("/status", status_handler)])
    return app

async def main() -> None:
    # 웹 서버와 봇을 동시에 실행
    runner = web.AppRunner(create_web_app())
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", 8080)
    await site.start()
    await bot.start(os.getenv("DISCORD_TOKEN"))

asyncio.run(main())
```

이 코드는 `asyncio.run` 내부에서 웹 서버와 봇을 함께 실행합니다. `/status`에 GET 요청을 보내면 JSON으로 상태가 반환됩니다. 대시보드 페이지를 작성하고 인증을 적용하면 관리자가 웹에서 봇 설정을 변경할 수 있습니다.

## FastAPI를 이용한 REST API

`FastAPI`는 타입 힌트를 활용해 문서화된 REST API를 쉽게 작성할 수 있는 프레임워크입니다. 다음은 봇의 기본 정보를 반환하는 엔드포인트를 정의한 예제입니다:

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/botinfo")
async def bot_info():
    return {
        "guilds": len(bot.guilds),
        "commands": len(bot.commands),
    }
```

FastAPI 서버를 `uvicorn`으로 실행하면 Swagger UI를 통해 API를 테스트할 수 있습니다. 단, 봇과 함께 실행할 때는 `asyncio.gather()` 또는 별도의 스레드를 사용해 둘을 동시에 돌려야 합니다.

## 주의 사항

- 디스코드 봇 토큰이나 민감한 데이터는 API를 통해 노출되지 않도록 주의합니다.
- 웹 서버를 함께 실행하면 봇의 이벤트 루프를 공유하므로, CPU 집약적인 작업을 웹 요청에서 수행하지 않도록 합니다.
- 비동기 데이터베이스와 연동해 설정을 저장/읽기하면 대시보드를 통해 실시간으로 봇을 제어할 수 있습니다.

이처럼 비동기 웹 프레임워크를 활용하면 봇의 기능을 확장하고 다른 서비스와 손쉽게 통합할 수 있습니다.

