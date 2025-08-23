# 선택 메뉴

**선택 메뉴(select menu)**는 여러 옵션 중에서 하나 또는 여러 개를 선택하게 해 주는 컴포넌트입니다. 버튼과 달리 드롭다운 형태로 많은 선택지를 깔끔하게 담을 수 있으며, 사용자 입력을 구조화된 값으로 받을 수 있습니다. `discord.ui.Select` 클래스를 사용해 메뉴를 정의하고, `discord.SelectOption` 객체를 통해 각 옵션을 설정합니다.

## 1. 기본 선택 메뉴 만들기

다음 예제는 간단한 과일 선택 메뉴를 만드는 방법을 보여 줍니다. `min_values`와 `max_values`를 1로 설정하면 사용자가 한 번에 하나의 옵션만 선택할 수 있습니다. `placeholder`는 아무 것도 선택하지 않았을 때 표시되는 메시지입니다.

```python
class FruitSelect(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label='사과', description='달콤한 사과입니다.', value='apple'),
            discord.SelectOption(label='바나나', description='노란 바나나입니다.', value='banana'),
            discord.SelectOption(label='포도', description='포도 한 송이.', value='grape'),
        ]
        super().__init__(placeholder='과일을 선택하세요...', min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        choice = self.values[0]  # 선택된 값
        await interaction.response.send_message(f'선택한 과일: {choice}', ephemeral=True)

class FruitView(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(FruitSelect())

@bot.command()
async def select_fruit(ctx):
    await ctx.send('과일을 골라주세요:', view=FruitView())
```

`self.values`는 리스트 형태로 선택된 값을 담고 있습니다. `min_values=1`, `max_values=1`이면 반드시 하나만 선택해야 합니다. 여러 값을 선택할 수 있도록 허용하려면 `max_values`를 2 이상으로 설정합니다.

## 2. 다중 선택과 기본값

선택 메뉴는 여러 옵션을 동시에 선택할 수 있도록 할 수 있습니다. 아래 예제는 역할 부여를 위한 다중 선택 메뉴로, 기본값을 지정해 이미 선택된 역할을 표시합니다:

```python
class RoleSelect(discord.ui.Select):
    def __init__(self, member: discord.Member):
        options = []
        for role in member.guild.roles:
            if role.is_default() or role.managed:
                continue
            options.append(discord.SelectOption(label=role.name, value=str(role.id), default=role in member.roles))
        super().__init__(placeholder='역할을 선택하거나 해제하세요', min_values=0, max_values=min(25, len(options)), options=options)

    async def callback(self, interaction: discord.Interaction):
        selected_role_ids = [int(v) for v in self.values]
        # 역할 추가/제거 로직 구현
        await interaction.response.send_message('역할이 업데이트되었습니다.', ephemeral=True)

class RoleView(discord.ui.View):
    def __init__(self, member):
        super().__init__()
        self.add_item(RoleSelect(member))
```

기본값을 지정하면 사용자가 이미 가지고 있는 역할이 선택된 상태로 표시됩니다. 최대 옵션 수는 25개이므로, 서버의 역할 수가 많다면 적절히 필터링해야 합니다.

## 3. 동적 옵션과 사용자 맞춤 메뉴

선택 메뉴의 옵션은 런타임에 동적으로 생성할 수 있습니다. 예를 들어 서버의 채널 목록을 불러와 선택 메뉴로 제공하거나, API 결과를 선택지로 제시할 수 있습니다. `channel_types`를 사용하면 선택 메뉴가 특정 채널 유형만 선택하도록 제한할 수도 있습니다.

```python
class ChannelSelect(discord.ui.ChannelSelect):
    def __init__(self):
        super().__init__(placeholder='텍스트 채널을 선택하세요', channel_types=[discord.ChannelType.text])

    async def callback(self, interaction, channel):
        await interaction.response.send_message(f'{channel.mention} 채널을 선택했습니다.', delete_after=5)

view = discord.ui.View()
view.add_item(ChannelSelect())
await ctx.send('채널을 선택하세요:', view=view)
```

`discord.ui.ChannelSelect`는 특정 유형의 채널만 선택하도록 제한할 수 있는 특수화된 선택 메뉴입니다.

## 4. 콜백과 반응 처리

선택 메뉴의 `callback()` 메서드는 선택이 확정된 후 호출됩니다. `interaction.response.send_message()`나 `interaction.response.edit_message()`를 사용해 결과를 전달할 수 있으며, `ephemeral=True` 옵션으로 호출자에게만 보여줄 수 있습니다. 또한, `View.interaction_check()` 메서드를 오버라이드하여 권한을 검사하거나 다른 제한을 적용할 수 있습니다.

선택 메뉴를 적절히 사용하면 복잡한 설정이나 사용자 선택을 간편하게 처리할 수 있습니다. 다음 장에서는 뷰(View)의 기본 사용법을 소개하고, 여러 UI 컴포넌트를 함께 사용하는 방법을 설명합니다.



