# 체크와 권한 관리

봇 명령어를 설계할 때는 특정 명령어를 관리자나 특정 역할을 가진 사용자만 실행하도록 제한해야 할 때가 많습니다. `discord.ext.commands` 모듈은 다양한 **체크(check) 데코레이터**를 제공하여 명령어 실행 권한을 세밀하게 제어할 수 있도록 합니다.

## 1. 역할 기반 체크

`@commands.has_role(*role_names)` 데코레이터는 명령 호출자가 특정 역할을 가지고 있는지 검사합니다. 하나의 문자열이나 역할 ID를 넘길 수 있으며, 목록을 전달하면 해당 역할 중 하나라도 보유한 경우 통과합니다. 예를 들면:

```python
from discord.ext import commands

@bot.command()
@commands.has_role('관리자')
async def admin_only(ctx):
    await ctx.send('이 명령은 관리자만 실행할 수 있습니다.')

@bot.command()
@commands.has_any_role('모더레이터', 'Helper')
async def multi_role(ctx):
    await ctx.send('모더레이터 또는 헬퍼 역할을 가진 사용자가 실행할 수 있습니다.')
```

역할 이름 대신 역할 ID(`int`)를 사용할 수도 있습니다. 이는 동일한 이름의 역할이 여러 서버에 있을 때 유용합니다.

## 2. 권한 기반 체크

`@commands.has_permissions(**perms)`는 사용자가 특정 Discord **권한(permission)** 을 갖고 있는지 검증합니다. 예를 들어, 메시지를 관리할 권한(`manage_messages`)을 가진 사용자만 명령을 실행하도록 할 수 있습니다:

```python
@bot.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount: int):
    deleted = await ctx.channel.purge(limit=amount)
    await ctx.send(f'{len(deleted)}개의 메시지를 삭제했습니다.', delete_after=5)
```

반대로 봇이 특정 권한을 가지고 있어야 명령을 실행할 수 있도록 하려면 `@commands.bot_has_permissions()` 데코레이터를 사용합니다. 이는 봇 계정의 권한을 검증합니다.

## 3. 소유자 체크와 채널 제한

특정 명령을 봇 **소유자**만 사용할 수 있게 하려면 `@commands.is_owner()`를 사용합니다. 봇 토큰을 가진 계정과 일치하는 사용자만 명령을 실행할 수 있습니다. 또한 `@commands.guild_only()`와 `@commands.dm_only()` 데코레이터로 명령을 길드 채팅 또는 DM으로 제한할 수 있습니다.

## 4. 사용자 정의 체크

내장 데코레이터로 충분하지 않은 경우 **사용자 정의 체크 함수**를 정의할 수 있습니다. `commands.check()` 데코레이터는 호출자 정의 검사 함수를 전달받습니다. 이 함수는 컨텍스트를 인자로 받아 불리언 값을 반환해야 하며, 예외를 발생시키면 명령이 실패합니다. 예를 들어, 명령 호출자가 다른 봇이 아닌 일반 사용자만이 실행 가능하도록 제한하는 체크를 정의해 보겠습니다:

```python
def is_not_bot():
    async def predicate(ctx):
        return not ctx.author.bot
    return commands.check(predicate)

@bot.command()
@is_not_bot()
async def user_only(ctx):
    await ctx.send('이 명령은 봇 계정이 아닌 사용자만 실행할 수 있습니다.')
```

사용자 정의 체크는 다른 체크와 조합하여 복잡한 조건을 만들 수 있습니다. 체크 데코레이터는 위에서 아래로 평가되며, 하나라도 실패하면 다음 체크가 실행되지 않고 예외가 발생합니다.

## 5. 오류 처리

체크가 실패하면 Discord.py는 `commands.CheckFailure` 계열 예외를 발생시키며, 이를 처리하기 위해 전역적으로 `on_command_error` 이벤트를 구현하거나 명령어별로 `@command.error` 데코레이터를 사용할 수 있습니다. 다음 예시는 권한 체크 실패 시 사용자에게 친절한 안내 메시지를 보내는 방법을 보여줍니다:

```python
@clear.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send('메시지 삭제 권한이 없습니다.')
    elif isinstance(error, commands.BotMissingPermissions):
        await ctx.send('봇에 메시지 삭제 권한을 부여해주세요.')
    else:
        raise error
```

이 장에서는 명령어 실행 조건을 제한하는 다양한 체크를 소개했습니다. 다음 장에서는 봇의 기능을 모듈화하는 **코그(Cog)** 구조를 살펴보겠습니다【258384405016557†L27-L44】.



