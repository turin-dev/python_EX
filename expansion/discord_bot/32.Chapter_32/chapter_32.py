"""HTTP 통합 예제.

`aiohttp`를 사용하여 외부 API에서 데이터를 가져오는 명령어와, 세션을 재사용하는 방법을 보여 줍니다.
"""

import aiohttp
import discord
from discord.ext import commands


bot = commands.Bot(command_prefix="!", intents=discord.Intents.default())
bot.http_session: aiohttp.ClientSession | None = None


@bot.event
async def on_ready() -> None:
    # 봇 시작 시 세션을 생성합니다.
    if bot.http_session is None:
        bot.http_session = aiohttp.ClientSession()
    print("HTTP 세션이 초기화되었습니다.")


@bot.command(name="날씨")
async def weather(ctx: commands.Context, *, city: str) -> None:
    """도시의 현재 기온을 반환합니다."""
    session = bot.http_session or aiohttp.ClientSession()
    async with session.get(f"https://wttr.in/{city}?format=j1") as resp:
        if resp.status != 200:
            await ctx.send("날씨 정보를 가져오는 데 실패했습니다.")
            return
        data = await resp.json()
    temp_c = data["current_condition"][0]["temp_C"]
    await ctx.send(f"{city}의 현재 기온은 {temp_c}°C 입니다.")


@bot.command(name="티켓")
async def create_ticket(ctx: commands.Context, *, desc: str) -> None:
    """설명으로 새 티켓을 생성하고 ID를 반환합니다."""
    session = bot.http_session or aiohttp.ClientSession()
    payload = {"user": ctx.author.id, "desc": desc}
    headers = {"Authorization": "Bearer YOUR_API_KEY"}
    async with session.post("https://api.example.com/tickets", json=payload, headers=headers) as resp:
        try:
            resp.raise_for_status()
        except aiohttp.ClientResponseError as e:
            await ctx.send(f"API 오류: {e.status}")
            return
        result = await resp.json()
    await ctx.send(f"티켓이 생성되었습니다. ID: {result.get('ticket_id')}")


@bot.event
async def on_close() -> None:
    # 봇 종료 시 세션을 닫습니다.
    if bot.http_session is not None:
        await bot.http_session.close()


if __name__ == "__main__":
    # bot.run("YOUR_TOKEN")
    pass