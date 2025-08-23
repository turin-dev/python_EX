# 21장 – 오류 처리와 예외 관리

명령어를 만들다 보면 사용자가 잘못된 입력을 전달하거나 특정 조건을 만족하지 않아 오류가 발생하는 경우가 많습니다. `discord.py`는 기본적으로 예외를 발생시키며, 아무런 처리가 없으면 콘솔에 스택 트레이스를 출력할 뿐입니다. 사용자 경험을 향상시키려면 명령어 수준이나 봇 전체 수준에서 오류를 포착하고 적절한 안내 메시지를 제공해야 합니다. 이 장에서는 전역 오류 핸들러와 명령어별 오류 핸들러를 구현하고, 자주 발생하는 예외 유형을 소개합니다.

## 전역 오류 핸들러 구현

가장 간단한 방법은 `commands.Bot` 또는 `discord.Client` 인스턴스에 이벤트 리스너로 `on_command_error`를 정의하는 것입니다. 이 핸들러는 모든 명령에서 발생한 예외를 포착해 실행됩니다. 특정 오류 유형을 분기해 사용자에게 친절한 메시지를 출력하고, 예상하지 못한 오류는 개발자가 디버깅할 수 있도록 다시 발생시키는 것이 좋습니다【104993650755089†L47-L112】.

```python
from discord.ext import commands

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

@bot.event
async def on_command_error(ctx, error):
    # 필수 인자가 누락된 경우
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("필수 인자가 누락되었습니다. 도움말을 확인하세요.")
    # 정의되지 않은 명령
    elif isinstance(error, commands.CommandNotFound):
        await ctx.send("해당 명령어를 찾을 수 없습니다.")
    # 권한 부족
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send("이 명령을 실행할 권한이 없습니다.")
    else:
        # 예기치 못한 오류는 로깅 후 재발생시켜 개발자가 인지할 수 있도록 합니다.
        await ctx.send(f"알 수 없는 오류가 발생했습니다: {error}")
        raise error
```

핸들러는 예외의 구체적인 타입을 검사하여 각기 다른 메시지를 보낼 수 있습니다. `commands.MissingRequiredArgument`, `commands.BadArgument`, `commands.MissingPermissions` 등 다양한 예외가 존재합니다.

## 명령어별 오류 처리

특정 명령에만 적용되는 오류 처리를 구현하고 싶다면 `@command.error` 데코레이터를 사용할 수 있습니다. 이 핸들러는 전역 핸들러보다 우선적으로 실행됩니다. 예를 들어 나이를 숫자로 변환하는 명령에서 오류를 처리하려면 다음과 같이 작성할 수 있습니다.

```python
@bot.command()
async def 성인(ctx, 나이: int):
    if 나이 >= 19:
        await ctx.send("성인이십니다.")
    else:
        await ctx.send("미성년자입니다.")

@성인.error
async def 성인_error(ctx, error):
    if isinstance(error, commands.BadArgument):
        await ctx.send("나이는 숫자로 입력해 주세요.")
```

이처럼 오류 처리를 구조화하면 사용자에게 친절한 피드백을 제공할 수 있습니다. 더 세밀한 제어가 필요할 때는 코그의 `cog_before_invoke`나 `cog_after_invoke`를 활용하여 명령 실행 전후에 검증과 정리 작업을 수행할 수 있습니다【258384405016557†L27-L44】.

## 요약

오류 처리는 디스코드 봇의 안정성과 사용자 경험을 좌우합니다. 전역 오류 핸들러를 구현해 예상치 못한 예외를 포착하고, 명령어별 핸들러로 입력 검증과 명확한 안내를 제공하세요. 또한 `discord.Intents`에서 필요한 이벤트만 활성화하여 봇이 처리해야 할 데이터의 양을 줄이고 보안을 강화하세요【666664033931420†L32-L45】.

