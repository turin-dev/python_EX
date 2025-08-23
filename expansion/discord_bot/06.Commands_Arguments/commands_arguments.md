# 명령어 인자와 타입 변환

명령어 함수는 위치 인자와 키워드 인자를 받아 사용자 입력을 처리할 수 있습니다. `discord.ext.commands`는 함수 시그니처를 분석하여 문자열 인자를 지정된 타입으로 **자동 변환**합니다. 이 섹션에서는 다양한 인자 유형, 기본값, 가변 인자 처리, 그리고 오류 처리 방법을 설명합니다.

## 1. 기본 타입 컨버터

명령어 함수의 매개변수에 **타입 힌트**를 지정하면, Discord.py는 문자열 인자를 해당 타입으로 변환하려고 시도합니다. 예를 들어, 아래 예제에서 `member` 매개변수의 타입을 `discord.Member`로 지정하면 멘션이나 ID 문자열이 자동으로 `Member` 객체로 변환됩니다:

```python
@bot.command()
async def greet(ctx, member: discord.Member):
    """지정한 멤버에게 인사합니다."""
    await ctx.send(f"{member.display_name}님, 안녕하세요!")
```

다음과 같은 기본 컨버터가 제공됩니다:

- `int`, `float`, `str`: 숫자나 문자열로 변환합니다.
- `discord.Member`, `discord.User`: 멘션이나 ID를 Discord 사용자 객체로 변환합니다.
- `discord.TextChannel`, `discord.VoiceChannel`: 채널 멘션이나 ID를 채널 객체로 변환합니다.
- `discord.Role`: 역할 멘션 또는 ID를 역할 객체로 변환합니다.
- `discord.Guild`: 서버 ID를 길드 객체로 변환합니다.

컨버전이 실패하면 `commands.BadArgument` 예외가 발생하며, 봇은 사용자가 올바른 형식을 입력하도록 안내하는 메시지를 보냅니다.

## 2. 기본값과 선택적 인자

파이썬 함수처럼 명령어에도 기본값을 지정할 수 있습니다. 기본값이 있는 매개변수는 선택적으로 입력할 수 있으며, 입력하지 않으면 기본값이 사용됩니다:

```python
@bot.command()
async def repeat(ctx, message: str, times: int = 1):
    for _ in range(times):
        await ctx.send(message)
```

`times` 인자에 기본값 `1`이 지정되어 있기 때문에 `/repeat 안녕하세요`와 같이 호출하면 한 번만 메시지를 전송합니다.

## 3. 가변 인자와 나머지 문자열

하나의 명령어에서 가변 개수의 인자를 받을 때는 `*args`를 사용합니다. 이 경우 각 단어가 별도의 인자로 전달됩니다. 전체 문자열을 하나의 인자로 받고 싶다면 **나머지 인자** 구문 `*` 다음에 변수명을 써서 마지막 매개변수로 지정합니다:

```python
@bot.command()
async def sum_numbers(ctx, *numbers: int):
    """여러 개의 정수를 더합니다."""
    total = sum(numbers)
    await ctx.send(f"합계: {total}")

@bot.command()
async def say(ctx, *, content: str):
    """사용자가 입력한 내용을 그대로 출력합니다."""
    await ctx.send(content)
```

위에서 `sum_numbers` 명령은 `!sum_numbers 1 2 3 4`처럼 여러 숫자를 입력받아 모두 더한 값을 출력하고, `say` 명령은 접두사 이후의 모든 문자열을 `content`로 받아 전송합니다.

## 4. 사용자 정의 컨버터

복잡한 변환 로직이 필요한 경우 **컨버터 클래스**를 정의할 수 있습니다. 컨버터는 `commands.Converter`를 상속하고 `convert()` 메서드를 오버라이드하여 입력 문자열을 원하는 객체로 변환합니다. 예를 들어, 날짜 문자열을 `datetime.date` 객체로 변환하는 컨버터를 만들어 봅니다:

```python
from discord.ext import commands
import datetime as dt

class DateConverter(commands.Converter):
    async def convert(self, ctx, argument: str) -> dt.date:
        try:
            return dt.datetime.strptime(argument, '%Y-%m-%d').date()
        except ValueError:
            raise commands.BadArgument('날짜 형식이 올바르지 않습니다. YYYY-MM-DD 형식으로 입력하세요.')

@bot.command()
async def schedule(ctx, date: DateConverter, *, event: str):
    await ctx.send(f"{date.isoformat()}에 {event} 일정이 추가되었습니다.")
```

컨버터는 비동기적으로 동작하므로, 내부에서 데이터베이스 조회나 API 호출 등도 수행할 수 있습니다. 오류를 발생시키면 Discord.py가 사용자에게 오류 메시지를 반환합니다.

## 5. 오류 처리와 유효성 검사

인자 변환이나 검증 과정에서 오류가 발생할 수 있습니다. 명령어 함수 내부에서 예외를 처리하거나, `@command.error` 데코레이터를 사용해 별도의 오류 처리 함수를 정의할 수 있습니다. 예를 들어 `BadArgument` 예외를 포착하여 사용자에게 친절한 메시지를 보내는 방법은 다음과 같습니다:

```python
@add.error
async def add_error(ctx, error):
    if isinstance(error, commands.BadArgument):
        await ctx.send('숫자를 정확하게 입력하세요. 예: `!add 2 3`')
    else:
        raise error  # 다른 오류는 그대로 전파
```

입력 값의 범위를 제한하고 싶다면 `commands.Range`와 같은 유틸리티를 사용할 수 있습니다. 예를 들어 `volume` 명령어에서 볼륨을 0~100 사이의 정수로 제한하려면 `volume: commands.Range[int, 0, 100]`처럼 작성합니다.

이 장에서는 명령어 인자 처리와 타입 컨버터의 기본을 살펴보았습니다. 다음 장에서는 명령어 실행 조건과 권한 체크를 적용해 봇의 보안을 강화하는 방법을 소개합니다.



