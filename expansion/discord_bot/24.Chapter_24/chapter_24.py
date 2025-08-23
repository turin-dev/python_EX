"""데이터 저장 예제.

이 모듈은 JSON 파일에 데이터를 읽고 쓰는 방법을 보여 줍니다. 명령어를 통해
사용자의 설정을 업데이트하고, 변경사항을 파일에 저장합니다.
"""

import json
from pathlib import Path
import discord
from discord.ext import commands


CONFIG_PATH = Path("config.json")


def load_config() -> dict:
    """설정 파일을 읽어 딕셔너리를 반환합니다."""
    if CONFIG_PATH.exists():
        with CONFIG_PATH.open("r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_config(data: dict) -> None:
    """설정 딕셔너리를 파일에 저장합니다."""
    with CONFIG_PATH.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


bot = commands.Bot(command_prefix="!", intents=discord.Intents.default())

# 전역 설정을 로드합니다.
config = load_config()


@bot.command()
async def set_greeting(ctx: commands.Context, *, greeting: str) -> None:
    """봇이 사용할 인사말을 설정합니다."""
    config["greeting"] = greeting
    save_config(config)
    await ctx.send(f"인사말이 '{greeting}'(으)로 업데이트되었습니다.")


@bot.command()
async def greet(ctx: commands.Context) -> None:
    """저장된 인사말을 전송합니다."""
    greeting = config.get("greeting", "안녕하세요!")
    await ctx.send(greeting)


if __name__ == "__main__":
    # 토큰을 입력하여 실행하세요.
    # bot.run("YOUR_TOKEN")
    pass