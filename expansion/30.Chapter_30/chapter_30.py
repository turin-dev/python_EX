"""확장 로딩/재로드 예제.

오너 전용 명령을 사용하여 봇의 확장을 로드, 언로드, 재로드할 수 있습니다.
"""

import discord
from discord.ext import commands


bot = commands.Bot(command_prefix="!", intents=discord.Intents.default())


@bot.command(name="load")
@commands.is_owner()
async def load_extension(ctx: commands.Context, extension: str) -> None:
    """지정한 확장을 로드합니다."""
    try:
        bot.load_extension(extension)
    except commands.ExtensionAlreadyLoaded:
        await ctx.send("이미 로드되어 있습니다. reload 명령을 사용하세요.")
    except commands.ExtensionFailed as e:
        await ctx.send(f"로드 실패: {e}")
    else:
        await ctx.send(f"{extension} 확장이 로드되었습니다.")


@bot.command(name="unload")
@commands.is_owner()
async def unload_extension(ctx: commands.Context, extension: str) -> None:
    """지정한 확장을 언로드합니다."""
    try:
        bot.unload_extension(extension)
    except commands.ExtensionNotLoaded:
        await ctx.send("해당 확장이 로드되어 있지 않습니다.")
    else:
        await ctx.send(f"{extension} 확장이 언로드되었습니다.")


@bot.command(name="reload")
@commands.is_owner()
async def reload_extension(ctx: commands.Context, extension: str) -> None:
    """지정한 확장을 재로드합니다."""
    try:
        bot.reload_extension(extension)
    except commands.ExtensionNotLoaded:
        await ctx.send("확장이 로드되지 않았습니다. 먼저 load 명령을 사용하세요.")
    except commands.ExtensionFailed as e:
        await ctx.send(f"재로드 실패: {e}")
    else:
        await ctx.send(f"{extension} 확장이 재로드되었습니다.")


if __name__ == "__main__":
    # bot.run("YOUR_TOKEN")
    pass