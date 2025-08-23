"""슬래시 명령 그룹 예제.

수학 연산을 그룹과 서브커맨드로 구현하여 `/수학 덧셈`과 `/수학 곱셈` 명령을 제공합니다.
"""

import discord
from discord import app_commands
from discord.ext import commands


class MathGroup(app_commands.Group):
    """수학 관련 슬래시 명령 그룹."""

    def __init__(self) -> None:
        super().__init__(name="수학", description="기본 수학 함수")

    @app_commands.command(name="덧셈", description="두 수를 더합니다")
    @app_commands.describe(a="첫 번째 정수", b="두 번째 정수")
    async def add(self, interaction: discord.Interaction, a: int, b: int) -> None:
        await interaction.response.send_message(f"{a} + {b} = {a + b}")

    @app_commands.command(name="곱셈", description="두 수를 곱합니다")
    async def multiply(self, interaction: discord.Interaction, a: int, b: int) -> None:
        await interaction.response.send_message(f"{a} × {b} = {a * b}")


bot = commands.Bot(command_prefix="!")


@bot.event
async def on_ready() -> None:
    # 그룹을 커맨드 트리에 추가하고 동기화합니다.
    bot.tree.add_command(MathGroup())
    await bot.tree.sync()
    print("수학 그룹 명령이 동기화되었습니다.")


if __name__ == "__main__":
    # bot.run("YOUR_TOKEN")
    pass