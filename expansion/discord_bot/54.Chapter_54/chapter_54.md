# 하이브리드 명령과 명령 그룹

봇을 개발하다 보면 슬래시 명령과 접두사 명령을 모두 제공하고 싶을 때가 있습니다. `discord.py`에서는 **하이브리드 명령**(`@bot.hybrid_command`)을 이용해 하나의 함수로 두 종류의 명령을 동시에 구현할 수 있고, 연관된 명령어들을 **명령 그룹**으로 묶어 관리할 수 있습니다.

## 하이브리드 명령 정의

하이브리드 명령은 `commands.Bot` 또는 `commands.Cog`에서 정의하며, 첫 번째 인자는 항상 `ctx` 또는 `interaction` 객체입니다. 슬래시 명령으로 등록되면서 접두사 명령도 유지되므로, 사용자에게 친숙한 사용성을 제공합니다. 아래 예제는 `hello`라는 하이브리드 명령을 정의한 것입니다:

```python
from discord.ext import commands

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

@bot.hybrid_command(name="hello", description="인사를 합니다")
async def hello(ctx: commands.Context) -> None:
    await ctx.send(f"안녕하세요 {ctx.author.display_name}님!")
```

이 명령은 슬래시(`/hello`)와 접두사(`!hello`) 모두로 호출할 수 있으며, 봇은 두 호출을 동일하게 처리합니다. 슬래시 명령을 사용하려면 봇이 준비된 후 `await bot.tree.sync()`로 명령을 동기화해야 합니다.

## 하이브리드 명령 그룹

관련 명령을 논리적으로 묶을 때는 하이브리드 명령 그룹을 사용합니다. 그룹은 `@bot.hybrid_group()` 데코레이터로 생성하고, 내부에 여러 서브커맨드를 정의할 수 있습니다. 예를 들어 설정 값을 조회/변경하는 명령을 묶을 수 있습니다:

```python
@bot.hybrid_group(name="설정", description="봇 설정 명령어 그룹")
async def config(ctx: commands.Context) -> None:
    if not ctx.invoked_subcommand:
        await ctx.send("사용 가능한 서브커맨드: 조회, 변경")

@config.command(name="조회")
async def config_get(ctx: commands.Context, key: str) -> None:
    value = CONFIG.get(key, "설정되지 않음")
    await ctx.send(f"{key} = {value}")

@config.command(name="변경")
async def config_set(ctx: commands.Context, key: str, value: str) -> None:
    CONFIG[key] = value
    await ctx.send(f"{key}가 {value}로 설정되었습니다")
```

위 예제에서 그룹 이름과 서브커맨드 이름은 한글로 지정했지만, 내부적으로는 영문 이름으로 등록됩니다. 슬래시 버전에서도 같은 이름으로 호출되며, 영어 알파벳과 숫자·하이픈만 사용할 수 있습니다. 서브커맨드는 슬래시 UI에서 하위 옵션으로 나타납니다.

## 팁과 주의사항

- 명령 그룹 안에서 `ctx.invoked_subcommand`를 사용하면 사용자가 하위 명령 없이 그룹만 호출한 경우를 감지하여 도움말을 표시할 수 있습니다.
- 하이브리드 명령에도 `@commands.has_permissions()` 등 체크 데코레이터를 사용할 수 있습니다.
- 슬래시 명령 동기화는 길드 단위 또는 글로벌 단위로 수행할 수 있으며, 개발 중에는 특정 길드에만 동기화하는 것이 빠릅니다.

하이브리드 명령과 그룹을 활용하면 동일한 코드로 다양한 인터페이스를 제공할 수 있어 유지보수가 간편해집니다. 명령 정의 시 타입 힌트를 활용하면 인자 변환이 자동으로 이루어집니다【104993650755089†L47-L112】.

