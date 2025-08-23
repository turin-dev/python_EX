"""
50장 – 고급 자동완성 예제

이 모듈은 슬래시 명령 매개변수에 대해 동적 자동완성을 구현하는 방법을 보여준다.
"""

import discord
from discord import app_commands
from discord.ext import commands


async def fruit_autocomplete(interaction: discord.Interaction, current: str) -> list[app_commands.Choice[str]]:
    """사용자가 입력하는 문자열을 기준으로 과일 목록을 반환한다."""
    fruits = ["Banana", "Pineapple", "Apple", "Watermelon", "Melon", "Cherry"]
    # current 문자열이 포함된 과일만 반환하고 최대 25개 제한
    return [
        app_commands.Choice(name=fruit, value=fruit)
        for fruit in fruits if current.lower() in fruit.lower()
    ][:25]


class FruitCog(commands.Cog):
    """과일 자동완성 슬래시 명령을 제공하는 코그."""

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="과일선택", description="좋아하는 과일을 입력합니다")
    @app_commands.autocomplete(fruit=fruit_autocomplete)
    async def fruits(self, interaction: discord.Interaction, fruit: str) -> None:
        await interaction.response.send_message(f"선택한 과일은 {fruit} 입니다")


async def setup(bot: commands.Bot) -> None:
    """봇에 과일 자동완성 코그를 등록한다."""
    await bot.add_cog(FruitCog(bot))

