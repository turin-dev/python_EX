"""웹 대시보드와 API 통합 예제.

이 모듈은 aiohttp를 사용하여 간단한 상태 API를 제공하는 웹 서버를
만들고, 이를 디스코드 봇과 동일한 이벤트 루프에서 실행하는
예제입니다. 실제 사용에서는 인증과 더 많은 엔드포인트를 추가할
수 있습니다.
"""

import os
import asyncio
from aiohttp import web
import discord
from discord.ext import commands


bot = commands.Bot(command_prefix="!", intents=discord.Intents.default())


async def status_handler(request: web.Request) -> web.Response:
    """봇의 상태 정보를 JSON으로 반환합니다."""
    return web.json_response({
        "online": bot.is_ready(),
        "guild_count": len(bot.guilds),
    })


def create_web_app() -> web.Application:
    app = web.Application()
    app.add_routes([web.get("/status", status_handler)])
    return app


async def start_services() -> None:
    """웹 서버와 봇을 동시에 시작합니다."""
    runner = web.AppRunner(create_web_app())
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", 8080)
    await site.start()
    await bot.start(os.getenv("DISCORD_TOKEN"))


if __name__ == "__main__":
    asyncio.run(start_services())

