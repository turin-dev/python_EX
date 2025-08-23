# 코그 기본

**코그(Cog)**는 관련 명령어와 이벤트 리스너를 하나의 클래스로 묶어 봇의 기능을 모듈화하는 구조입니다. 프로젝트가 커질수록 한 파일에 모든 명령을 두는 것은 관리가 어렵고, 재사용도 힘듭니다. 코그를 사용하면 명령어와 이벤트를 논리적으로 분리하고 유지보수를 쉽게 할 수 있습니다【258384405016557†L27-L44】.

## 1. 코그 클래스 정의

코그는 `commands.Cog`를 상속하는 클래스입니다. 생성자에서 봇 객체를 받아 저장할 수 있으며, 클래스 내부의 메서드에 데코레이터를 적용하여 명령어와 이벤트 리스너를 정의합니다. 다음은 간단한 환영 코그의 예입니다:

```python
from discord.ext import commands

class GreetingCog(commands.Cog):
    """환영 메시지와 인사 명령을 처리하는 코그"""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = member.guild.system_channel
        if channel:
            await channel.send(f'{member.mention}님, 서버에 오신 것을 환영합니다!')

    @commands.command(name='greet')
    async def greet_command(self, ctx, *, name: str = None):
        name = name or ctx.author.display_name
        await ctx.send(f'{name}님, 반갑습니다!')

def setup(bot: commands.Bot):
    bot.add_cog(GreetingCog(bot))
```

코그 파일은 일반적으로 모듈로 분리하여, `setup(bot)` 함수를 통해 봇에 코그를 등록합니다. `setup()` 함수는 코그를 인스턴스화하고 `bot.add_cog()`을 호출합니다. 이렇게 하면 다른 파일에서 `bot.load_extension('greeting_cog')`으로 코그를 동적으로 로드할 수 있습니다.

## 2. 코그 등록과 언로드

코그를 등록하려면 다음과 같이 확장 모듈을 불러옵니다:

```python
bot.load_extension('cogs.greeting_cog')
```

확장을 해제하려면 `bot.unload_extension('cogs.greeting_cog')`를 호출합니다. 확장 모듈은 `setup()` 함수 외에도 `teardown()` 함수를 정의할 수 있는데, 이는 언로드 시 실행되어 리소스를 정리할 수 있습니다. 또한 코그 클래스 내부에 `cog_unload()` 메서드를 정의하면 코그가 언로드될 때 실행됩니다【258384405016557†L87-L100】.

## 3. 코그에서 상태 유지와 공유

코그는 클래스 인스턴스이므로, `self.counter`처럼 인스턴스 변수를 통해 상태를 유지할 수 있습니다. 여러 명령어 간에 데이터를 공유하거나, 초기화 시 API 클라이언트와 같은 리소스를 생성하여 저장하는 데 사용할 수 있습니다. 예를 들어 API 키를 받아 데이터를 캐싱하는 코그를 만들 수 있습니다.

## 4. 체크와 코그 전용 권한

코그 클래스는 `cog_check()` 메서드를 정의하여 코그 내부 모든 명령에 적용되는 체크를 구현할 수 있습니다. 예를 들어, 특정 길드에서만 명령을 사용하도록 제한하거나, 봇 소유자만 접근하도록 지정할 수 있습니다. 또한 `cog_before_invoke()`와 `cog_after_invoke()` 메서드를 정의해 모든 명령 실행 전후에 공통 로직을 실행할 수 있습니다.

코그는 봇 명령어를 모듈화하고 재사용 가능한 구조로 만들 수 있게 해줍니다. 다음 장에서는 코그를 한 단계 더 발전시켜 고급 기능과 동적 로딩 기법을 살펴봅니다.



