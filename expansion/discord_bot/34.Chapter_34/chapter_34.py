"""다국어 지원 예제.

gettext를 사용한 문자열 번역과 슬래시 명령 로컬라이즈 예제를 포함합니다.
"""

import gettext
import discord
from discord.ext import commands
from discord import app_commands


# 번역 파일을 로드합니다. 실제 경로와 도메인을 설정하세요.
ko_translation = gettext.translation("messages", localedir="locales", languages=["ko"], fallback=True)
_ = ko_translation.gettext


bot = commands.Bot(command_prefix="!", intents=discord.Intents.default())


@bot.tree.command(
    name="greet",
    description="Greets the user",
    name_localizations={"ko": "인사"},
    description_localizations={"ko": "사용자에게 인사합니다"},
)
@app_commands.describe(name="Your name", name_localizations={"ko": "이름"})
async def greet(interaction: discord.Interaction, name: str) -> None:
    """사용자의 이름을 받아 인사합니다."""
    await interaction.response.send_message(_(f"Hello, {name}!"))


if __name__ == "__main__":
    # bot.run("YOUR_TOKEN")
    pass