# 50장 – 고급 자동완성 기능

슬래시 명령의 매개변수는 미리 정의된 선택지를 제공하거나, 사용자가 입력하는 값을 기반으로
**자동완성**(autocomplete) 제안을 보여줄 수 있습니다. 자동완성 콜백은 사용자의 현재 입력을
받아 동적으로 선택지를 반환하며, 최대 25개의 제안을 제공할 수 있습니다. 이 장에서는 자동완성
데코레이터와 구현 방법을 살펴봅니다.

## @app_commands.autocomplete 데코레이터

`discord.py`에서 자동완성을 구현하려면 슬래시 명령 콜백에 대해 `@<command>.autocomplete('param')` 데코레이터를 사용합니다. 공식 문서에 따르면 자동완성 콜백은 두 개의 인자를 받아야 합니다: **Interaction** 객체와 사용자가 현재 입력 중인 문자열입니다【716329102970593†L9699-L9743】. 함수는 최대 25개의 `app_commands.Choice` 객체를 포함하는 리스트를 반환해야 하며, 사용자가 제안을 무시하고 다른 값을 입력할 수 있다는 점에 유의해야 합니다【716329102970593†L9716-L9723】.

주요 사항:

* 자동완성 콜백은 **코루틴**이어야 하며, 반환 값은 `List[app_commands.Choice]`입니다【716329102970593†L9716-L9743】.
* 부모 명령의 **체크 decorators**는 자동완성에 적용되지 않습니다. 별도의 검증이 필요하면 자동완성 콜백에 직접 체크를 구현해야 합니다【716329102970593†L9711-L9714】.
* 사용자가 다른 값을 입력할 수 있으므로, 제안을 제한적 힌트로만 제공해야 합니다【716329102970593†L9716-L9723】.

## 예제: 동적 과일 자동완성

다음 예제에서는 `fruits` 명령에 대해 사용자가 과일 이름을 입력할 때 자동완성 제안을 제공합니다. 콜백은 현재 문자열에 포함된 과일만 반환하며, 사용자가 입력한 문자열과 대소문자 구분 없이 비교합니다.

```python
import discord
from discord import app_commands
from discord.ext import commands


async def fruit_autocomplete(
    interaction: discord.Interaction,
    current: str
) -> list[app_commands.Choice[str]]:
    fruits = ["Banana", "Pineapple", "Apple", "Watermelon", "Melon", "Cherry"]
    return [
        app_commands.Choice(name=fruit, value=fruit)
        for fruit in fruits if current.lower() in fruit.lower()
    ][:25]


class FruitCog(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="과일선택", description="좋아하는 과일을 입력합니다")
    @app_commands.autocomplete(fruit=fruit_autocomplete)
    async def fruits(self, interaction: discord.Interaction, fruit: str):
        await interaction.response.send_message(f"선택한 과일은 {fruit} 입니다")


async def setup(bot: commands.Bot):
    await bot.add_cog(FruitCog(bot))
```

`fruit_autocomplete`는 `Interaction`과 `current` 문자열을 받아 현재 입력한 값이 포함된 과일 목록을 반환합니다. `@app_commands.autocomplete(fruit=fruit_autocomplete)` 데코레이터는 `fruit` 인자의 자동완성 콜백을 등록합니다. 자동완성 콜백 내에서는 `interaction.namespace`를 사용하여 다른 인자의 값에 접근할 수 있습니다【716329102970593†L9707-L9709】.

## 고급 패턴: 데이터베이스 자동완성

실제 봇에서는 데이터베이스나 외부 API에서 결과를 가져와 자동완성 목록을 제공할 수 있습니다. 예를 들어 사용자에게 음성 채널을 선택하도록 할 때, 길드의 음성 채널 목록을 조회하여 25개 이하로 필터링합니다. 또한 캐싱을 도입하여 반복적인 DB 조회를 줄이고, 입력 길이에 따라 검색 범위를 조절하는 것이 좋습니다.

## 요약

자동완성 기능을 통해 사용자는 긴 명령 인자를 기억하지 않아도 쉽고 빠르게 입력할 수 있습니다. 자동완성 콜백은 `Interaction`과 현재 입력 문자열을 받아 최대 25개의 `Choice` 객체를 반환해야 하며, 사용자가 선택지를 무시할 수도 있습니다【716329102970593†L9699-L9743】. 데이터베이스와 연계하여 동적으로 목록을 생성하면 더욱 풍부한 사용자 경험을 제공할 수 있습니다.