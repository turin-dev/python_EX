# 기본 명령어

이 장에서는 `discord.ext.commands` 모듈이 제공하는 **명령어(Command) 시스템**의 기본 사용법을 설명합니다. 명령어는 사용자가 채팅에서 특정 접두사와 함께 입력하는 문자열을 인식하여, 봇이 정의된 함수(코루틴)를 실행하도록 합니다. `commands.Bot` 클래스는 `Client`를 상속하며 명령어와 관련된 많은 편의 기능을 제공합니다【104993650755089†L47-L112】.

## 1. Bot 인스턴스 생성

`commands.Bot`은 명령어 프리픽스와 Intents를 인자로 받아 생성합니다. 프리픽스는 명령어 앞에 붙는 문자열로, 사용자가 보낸 메시지 중 해당 접두사로 시작하는 내용만 명령어로 처리됩니다. 예를 들어, `!` 프리픽스를 사용하면 `!hello`와 같은 명령을 정의할 수 있습니다.

```python
from discord.ext import commands
import os
import discord

intents = discord.Intents.default()
intents.message_content = True  # 명령어 처리를 위해 필수

bot = commands.Bot(command_prefix='!', intents=intents, help_command=None)

@bot.event
async def on_ready():
    print(f"{bot.user} 준비 완료. {len(bot.guilds)}개의 서버에서 작동 중입니다.")

if __name__ == '__main__':
    bot.run(os.getenv('DISCORD_TOKEN'))
```

위 코드에서 `help_command=None`으로 지정하면 기본 도움말 명령어를 비활성화하고, 나중에 사용자 정의 도움말을 구현할 수 있습니다.

## 2. 명령어 정의

명령어는 `@bot.command()` 데코레이터를 사용해 정의합니다. 함수의 첫 번째 인자는 **컨텍스트(`ctx`)**로, 명령을 호출한 채널, 저자, 메시지 등의 정보를 담고 있습니다【104993650755089†L47-L112】. 기본적으로 명령어 이름은 함수 이름과 동일하지만, `name` 또는 `aliases` 매개변수로 별칭을 지정할 수 있습니다.

```python
@bot.command(name='hello', aliases=['hi', '안녕'])
async def hello_command(ctx: commands.Context):
    """인사 명령어: 사용자를 mention하여 인사를 돌려줍니다."""
    await ctx.send(f'{ctx.author.mention}님, 안녕하세요!')

@bot.command()
async def add(ctx, a: int, b: int):
    """두 정수를 더해서 결과를 출력합니다."""
    await ctx.send(f'{a} + {b} = {a + b}')
```

위 예제에서 `add` 명령어는 두 개의 정수를 인자로 받고, Discord.py의 타입 컨버터가 문자열 인자를 자동으로 정수로 변환합니다. 컨텍스트(`ctx`)는 `commands.Context` 객체이며 `send()`, `reply()` 등의 메서드를 제공합니다. 함수에 타입 힌트를 지정하지 않으면 인자는 문자열로 전달됩니다.

## 3. 동적 명령어 등록과 해제

명령어를 동적으로 추가하거나 삭제할 수도 있습니다. `commands.command()` 데코레이터로 명령어 객체를 만들고 `bot.add_command()` 또는 `bot.remove_command()`를 통해 관리합니다. 예를 들어 다음과 같이 명령어를 조건부로 등록할 수 있습니다:

```python
from discord.ext import commands

@commands.command(name='echo')
async def echo(ctx, *, content: str):
    await ctx.send(content)

if some_condition:
    bot.add_command(echo)  # 런타임에 명령어 추가
```

명령어를 삭제하려면 `bot.remove_command('echo')`를 호출합니다. 이러한 기능은 플러그인 구조나 관리 명령어를 구현할 때 유용합니다.

## 4. message_content 인텐트 활성화

명령어 시스템을 사용하려면 메시지 내용을 읽을 수 있어야 하기 때문에, **MESSAGE CONTENT INTENT**를 활성화해야 합니다【666664033931420†L86-L114】. 개발자 포털과 코드에서 모두 설정해야 하며, 그렇지 않으면 명령어가 작동하지 않을 수 있습니다. `discord.Bot`과 `commands.Bot` 모두 인텐트를 동일하게 처리합니다.

## 5. 추가 팁

- **대소문자 무시**: `commands.Bot(command_prefix='!', case_insensitive=True)`로 설정하면 명령어 이름의 대소문자를 구분하지 않습니다.
- **명령어 비활성화**: `@bot.command(hidden=True)`로 설정하면 `help` 명령어에서 숨길 수 있습니다.
- **도움말 커스터마이징**: `help_command`를 사용자 정의 클래스로 교체하여 명령어 도움말의 형식을 바꿀 수 있습니다. 이 방법은 추후 장에서 다룰 예정입니다.

이 장에서는 `commands.Bot`을 이용해 기본적인 명령어를 정의하고 실행하는 방법을 배웠습니다. 다음 장에서는 명령어 인자와 타입 컨버터를 보다 깊이 있게 살펴봅니다.



