"""예외 처리 예제.

이 스크립트는 명령어 실행 시 발생할 수 있는 오류를 포착하여
사용자에게 친절한 메시지를 보내는 방법을 보여 줍니다.
각 명령과 전역 수준에서 오류를 처리하는 패턴을 포함합니다.
"""

import discord
from discord.ext import commands

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())


@bot.command()
async def divide(ctx: commands.Context, a: float, b: float) -> None:
    """두 수를 나누어 결과를 반환합니다.

    `a`와 `b`에 숫자가 아닌 값이 전달되면 `BadArgument`가 발생하며,
    0으로 나누려고 하면 `ZeroDivisionError`가 발생합니다.
    """
    result = a / b
    await ctx.send(f"{a} / {b} = {result}")


@divide.error
async def divide_error(ctx: commands.Context, error: commands.CommandError) -> None:
    """`divide` 명령어의 오류를 처리합니다.

    여기서는 인자 형식 오류와 0으로 나눌 때의 오류를 포착하여
    사용자에게 이해하기 쉬운 메시지를 제공합니다.
    """
    if isinstance(error, commands.BadArgument):
        await ctx.send("숫자를 정확히 입력해 주세요.")
    elif isinstance(error, ZeroDivisionError):
        await ctx.send("0으로는 나눌 수 없습니다.")
    else:
        await ctx.send(f"알 수 없는 오류: {error}")


@bot.event
async def on_command_error(ctx: commands.Context, error: commands.CommandError) -> None:
    """전역 오류 핸들러.

    명령어별 핸들러가 존재하지 않을 때 호출되며,
    흔히 발생하는 예외를 분기 처리합니다.
    """
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("존재하지 않는 명령어입니다.")
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send("이 명령을 사용할 권한이 없습니다.")
    else:
        # 디버깅을 위해 예외를 다시 발생시킬 수 있습니다.
        raise error


if __name__ == "__main__":
    # 실행 시 실제 토큰을 입력하거나 환경 변수에서 읽어 옵니다.
    # bot.run(os.getenv("DISCORD_TOKEN"))
    pass