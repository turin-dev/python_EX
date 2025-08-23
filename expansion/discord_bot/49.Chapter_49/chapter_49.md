# 49장 – 하이브리드 명령

하이브리드 명령은 메시지 명령(command)과 슬래시 명령을 동시에 지원하는 명령을 의미합니다. 사용자는 채팅창에 접두사(`!`, `?` 등)와 함께 명령을 입력하거나, 슬래시 명령 UI에서 동일한 명령을 사용할 수 있습니다. 이를 통해 기존 명령과 새 인터랙션 기반 명령을 하나의 함수로 관리할 수 있습니다.

## hybrid_command 사용법

`discord.ext.commands`에서 제공하는 `@commands.hybrid_command()` 데코레이터를 사용하면 함수 하나로 두 종류의 명령을 모두 등록할 수 있습니다. 내부적으로는 `@commands.command()`와 `@discord.app_commands.command()`를 모두 적용하는 것과 유사합니다. 기본 명령어 시스템에서 설명한 것처럼, 명령 함수의 첫 번째 인자는 `ctx`이며 명령 실행 환경을 나타냅니다【104993650755089†L47-L112】.

주요 매개변수는 다음과 같습니다:

* **name** – 명령 이름. 지정하지 않으면 함수 이름을 사용합니다.
* **description** – 슬래시 명령 UI에 표시될 설명입니다.
* **with_app_command** – `False`로 설정하면 슬래시 명령으로 등록하지 않고 기존 메시지 명령으로만 동작하게 할 수 있습니다.
* **guild_ids** – 슬래시 명령을 특정 길드에만 등록하고 싶을 때 ID 목록을 전달합니다.

## 예제: 핑 명령 구현

다음 예제는 `@commands.hybrid_command()`를 사용하여 `/핑` 및 `!핑` 두 가지 방식으로 호출할 수 있는 명령을 정의합니다. 슬래시 명령 UI에 설명을 제공하고, 옵션으로 정수를 받아 반복 횟수를 지정할 수 있습니다.

```python
import discord
from discord.ext import commands


class PingCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.hybrid_command(name="핑", description="퐁!을 출력하는 명령", with_app_command=True)
    async def ping(self, ctx: commands.Context, times: int = 1):
        """times 인자만큼 퐁을 반복합니다."""
        times = max(1, min(times, 5))  # 1~5회 제한
        for _ in range(times):
            await ctx.reply("퐁!", mention_author=False)


async def setup(bot: commands.Bot):
    await bot.add_cog(PingCog(bot))
```

위 코드에서 `ping` 명령은 메시지 명령과 슬래시 명령으로 모두 등록됩니다. 슬래시 명령 호출 시에는 `times` 인자가 자동으로 파싱되며, 메시지 명령 호출 시에는 문자열 인자가 정수로 변환됩니다. `with_app_command=False`로 설정하면 슬래시 명령 등록을 건너뛸 수 있습니다.

## 하이브리드 체크와 오류 처리

하이브리드 명령에도 일반 명령과 동일한 체크 decorators (`@commands.has_permissions`, `@commands.is_owner`, `@commands.guild_only` 등)를 사용할 수 있습니다. 슬래시 명령으로 호출될 때는 `ctx.interaction` 속성을 통해 상호작용 객체에 접근할 수 있으며, 오류가 발생하면 `on_command_error` 또는 슬래시 버전의 `on_app_command_error`를 통해 처리해야 합니다.

## 요약

하이브리드 명령은 기존 명령 시스템과 새로운 슬래시 명령 시스템을 동시에 지원하여 사용자 경험을 향상시킵니다. `@commands.hybrid_command()` 데코레이터를 사용하면 두 명령을 하나의 함수로 작성할 수 있으며, 명령 이름과 설명, 길드 대상 등을 세밀하게 제어할 수 있습니다. 기본 명령 체계와 동일하게 체크와 오류 처리 로직을 구현할 수 있습니다【104993650755089†L47-L112】.