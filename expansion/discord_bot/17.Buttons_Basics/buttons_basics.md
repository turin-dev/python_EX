# 버튼 기본

버튼은 메시지에 클릭 가능한 UI 요소를 추가하여 사용자와 상호작용할 수 있도록 도와줍니다. `discord.ui.Button` 클래스를 사용하여 버튼을 정의하고, `discord.ui.View`에 추가한 뒤 메시지와 함께 전송합니다. 버튼은 **라벨**, **스타일**, **이모지**, **URL**, **커스텀 ID**, **비활성화 여부** 등을 설정할 수 있으며【716329102970593†L5969-L6031】, 콜백 메서드를 통해 클릭 이벤트를 처리합니다.

## 1. 버튼 정의와 뷰에 추가

가장 간단한 방법은 `discord.ui.Button`을 상속한 클래스에서 `callback()` 메서드를 오버라이드하는 것입니다. 아래 예제는 두 개의 버튼을 가진 뷰를 생성하고, 각각 다른 응답을 보내는 방법을 보여줍니다:

```python
import discord

class CounterView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=60)  # 60초 후 뷰가 비활성화됨
        self.value = 0

    @discord.ui.button(label='증가', style=discord.ButtonStyle.success)
    async def increment(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.value += 1
        await interaction.response.edit_message(content=f'값: {self.value}', view=self)

    @discord.ui.button(label='감소', style=discord.ButtonStyle.danger)
    async def decrement(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.value -= 1
        await interaction.response.edit_message(content=f'값: {self.value}', view=self)

@bot.command()
async def counter(ctx):
    view = CounterView()
    await ctx.send('버튼을 눌러 값을 변경하세요.', view=view)
```

`@discord.ui.button` 데코레이터는 버튼을 뷰에 추가하고, `callback` 메서드를 설정합니다. `style` 파라미터는 버튼의 색상과 모양을 결정합니다. Discord는 `primary`, `secondary`, `success`, `danger`, `link`의 다섯 가지 스타일을 제공합니다.

## 2. URL 버튼과 외부 링크

URL 버튼은 클릭 시 외부 링크로 이동합니다. 이 버튼은 `style=ButtonStyle.link`로 지정하며, `custom_id`를 사용할 수 없습니다. 예를 들어 깃허브 저장소로 이동하는 버튼을 만들려면 다음과 같이 작성합니다:

```python
url_button = discord.ui.Button(label='소스 코드 보기', url='https://github.com/your/repo')
view = discord.ui.View()
view.add_item(url_button)
await ctx.send('프로젝트 소스는 다음 링크에서 확인하세요:', view=view)
```

## 3. 버튼 행(row)과 배치

하나의 메시지에 최대 5개의 행(row)을 사용할 수 있으며, 각 행에는 최대 5개의 버튼을 배치할 수 있습니다【716329102970593†L6015-L6023】. 버튼을 선언할 때 `row` 매개변수를 지정하면 다른 행에 배치할 수 있으며, 레이아웃을 유연하게 조정할 수 있습니다. 예를 들어:

```python
class YesNoView(discord.ui.View):
    @discord.ui.button(label='예', style=discord.ButtonStyle.primary, row=0)
    async def yes(self, interaction, button):
        await interaction.response.send_message('예를 선택하셨습니다.')

    @discord.ui.button(label='아니오', style=discord.ButtonStyle.danger, row=1)
    async def no(self, interaction, button):
        await interaction.response.send_message('아니오를 선택하셨습니다.')
```

## 4. 영구적 뷰와 사용자 제한

뷰는 기본적으로 메시지가 삭제되거나 타임아웃이 지나면 비활성화됩니다. 봇을 재시작해도 버튼이 계속 작동하도록 하려면 **영구 뷰(persistent view)** 를 사용해야 합니다. 영구 뷰는 `timeout=None`으로 설정하고, 각 버튼에 `custom_id`를 지정해야 합니다. 그리고 봇 시작 시 `bot.add_view()`를 호출하여 뷰를 등록합니다.

사용자가 버튼을 클릭할 때 권한을 검사하려면 `View.interaction_check()` 메서드를 오버라이드합니다. 예를 들어, 명령을 호출한 사용자만 버튼을 사용할 수 있도록 제한할 수 있습니다:

```python
class OwnerOnlyView(discord.ui.View):
    def __init__(self, owner: discord.User):
        super().__init__()
        self.owner = owner

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user != self.owner:
            await interaction.response.send_message('이 버튼을 사용할 수 없습니다.', ephemeral=True)
            return False
        return True
```

## 5. 버튼 비활성화와 제거

버튼을 클릭한 후 더 이상 사용할 수 없도록 하려면 `button.disabled = True`로 설정하고 메시지를 업데이트해야 합니다. 또한, `View.remove_item()`으로 버튼을 동적으로 제거할 수도 있습니다. 사용자 경험을 위해 버튼 상태를 적절히 조절하세요.

이번 장에서는 기본적인 버튼 사용법과 레이아웃, 영구 뷰 및 권한 제한 등에 대해 설명했습니다. 다음 장에서는 버튼을 활용한 고급 인터랙션과 비동기 작업을 결합하는 방법을 알아봅니다.



