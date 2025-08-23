# 26장 – 슬래시 명령 그룹과 서브커맨드

슬래시 명령은 하나의 엔드포인트에 여러 기능을 묶어 단계적으로 옵션을 선택할 수 있는 **그룹(group)** 과 **서브커맨드(subcommand)** 를 지원합니다. 이를 사용하면 명령을 논리적 범주로 분류하고, 비슷한 기능을 하나의 명령 트리로 구성할 수 있습니다.

## 그룹 정의하기

`discord.app_commands` 모듈에서 `Group` 클래스를 사용하여 그룹을 정의할 수 있습니다. 그룹은 자체 콜백을 가지지 않으며, 하위 명령으로만 구성됩니다. 예를 들어 간단한 계산기를 그룹으로 만들고 덧셈과 곱셈을 서브커맨드로 추가할 수 있습니다.

```python
import discord
from discord import app_commands
from discord.ext import commands


class MathGroup(app_commands.Group):
    def __init__(self):
        super().__init__(name="수학", description="기본 수학 함수")

    @app_commands.command(name="덧셈", description="두 수를 더합니다")
    @app_commands.describe(a="첫 번째 정수", b="두 번째 정수")
    async def add(self, interaction: discord.Interaction, a: int, b: int):
        await interaction.response.send_message(f"{a} + {b} = {a + b}")

    @app_commands.command(name="곱셈", description="두 수를 곱합니다")
    async def multiply(self, interaction: discord.Interaction, a: int, b: int):
        await interaction.response.send_message(f"{a} × {b} = {a * b}")


bot = commands.Bot(command_prefix="!")


@bot.event
async def on_ready():
    # 그룹을 커맨드 트리에 등록하고 동기화
    bot.tree.add_command(MathGroup())
    await bot.tree.sync()
    print("슬래시 명령이 동기화되었습니다.")
```

위 예제는 `/수학 덧셈`과 `/수학 곱셈`이라는 두 개의 서브커맨드를 제공합니다. 서브커맨드의 인자는 일반 슬래시 명령과 동일하게 타입 힌트를 사용하며, `describe()` 데코레이터로 설명을 달 수 있습니다.

## 중첩 그룹

그룹 안에 하위 그룹을 중첩할 수도 있습니다. 예를 들어 `/관리 사용자 제거`와 같이 두 단계의 서브커맨드를 정의할 수 있습니다. 그러나 너무 깊은 계층 구조는 사용성이 떨어질 수 있으므로 두 단계 정도로 제한하는 것이 좋습니다. 또한 하위 그룹의 이름과 설명은 1–32자의 제한을 지켜야 하며, 명령어 이름에 대소문자와 공백이 허용되지 않습니다【104993650755089†L47-L112】.

## 기존 명령과 충돌 주의

슬래시 명령 그룹을 정의할 때 기존 명령 이름과 중복되지 않도록 주의해야 합니다. 또한 그룹과 서브커맨드 이름은 고유해야 하며, 다른 봇과 충돌하지 않도록 접두어를 명확히 설정하는 것이 좋습니다. 명령을 제거하거나 수정한 후에는 `await bot.tree.sync()`를 다시 호출하여 변경사항을 Discord에 반영해야 합니다.

## 요약

슬래시 명령 그룹을 사용하면 관련된 기능을 깔끔하게 묶을 수 있으며, 사용자에게 명확한 네비게이션을 제공합니다. `Group` 클래스를 상속해 서브커맨드를 정의하고, 봇이 준비되었을 때 커맨드 트리에 추가한 후 동기화하세요. 이름과 설명의 길이 제한과 고유성을 지키는 것을 잊지 마세요.

