"""
외부 API 통합 예제.

이 모듈은 두 가지 API 통합을 제공합니다:
  - OpenWeatherMap API를 사용해 도시의 현재 날씨를 조회
  - MyMemory 번역 API를 사용해 텍스트를 지정한 언어로 번역

`aiohttp`를 사용하여 비동기 HTTP 요청을 수행하며, 세마포어를 통해 동시에
수행되는 API 호출 수를 제한합니다. API 키는 환경 변수로 로드해야 합니다.
"""

from __future__ import annotations
import os
import asyncio
import aiohttp
import discord
from discord.ext import commands


OPENWEATHER_KEY = os.getenv("OPENWEATHER_API_KEY", "")


async def fetch_weather(city: str) -> str:
    if not OPENWEATHER_KEY:
        return "환경 변수 OPENWEATHER_API_KEY가 설정되지 않았습니다."
    params = {"q": city, "appid": OPENWEATHER_KEY, "units": "metric", "lang": "kr"}
    async with aiohttp.ClientSession() as session:
        async with session.get("https://api.openweathermap.org/data/2.5/weather", params=params) as resp:
            if resp.status != 200:
                return f"날씨 API 응답 오류: {resp.status}"
            data = await resp.json()
    desc = data["weather"][0]["description"]
    temp = data["main"]["temp"]
    return f"{city}의 현재 날씨: {desc}, {temp:.1f}°C"


async def translate_text(text: str, target_lang: str = "en") -> str:
    async with aiohttp.ClientSession() as session:
        async with session.get(
            "https://api.mymemory.translated.net/get",
            params={"q": text, "langpair": f"auto|{target_lang}"},
        ) as resp:
            if resp.status != 200:
                return f"번역 API 오류: {resp.status}"
            data = await resp.json()
    return data.get("responseData", {}).get("translatedText", "번역 실패")


class IntegrationCog(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.sem = asyncio.Semaphore(3)

    @commands.command(name="weather")
    async def weather(self, ctx: commands.Context, *, city: str) -> None:
        """도시의 날씨 정보를 조회합니다."""
        async with self.sem:
            result = await fetch_weather(city)
        await ctx.send(result)

    @commands.command(name="translate")
    async def translate(self, ctx: commands.Context, target_lang: str, *, text: str) -> None:
        """텍스트를 target_lang으로 번역합니다. 예: !translate en 안녕하세요"""
        async with self.sem:
            translation = await translate_text(text, target_lang)
        await ctx.send(f"번역 결과: {translation}")


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(IntegrationCog(bot))