# 버튼 고급 사용

기본 버튼 사용법을 익혔다면, 보다 정교한 인터랙션을 구현하기 위해 고급 기능을 활용할 수 있습니다. 이 장에서는 **행(row) 배치**, **권한 검사**, **영구적 뷰(persistent view)**, **버튼 상태 제어** 등을 상세히 설명합니다.

## 1. 행(row) 배치와 그리드 구성

메시지 하나에는 최대 5개의 행을 사용할 수 있으며 각 행에 최대 5개의 버튼을 배치할 수 있습니다【716329102970593†L6015-L6023】. 버튼을 선언할 때 `row` 매개변수를 사용하여 위치를 지정할 수 있습니다. 여러 행을 활용하면 버튼 그룹을 시각적으로 구분할 수 있습니다.

```python
class CalculatorView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=120)
        self.result = ''

    @discord.ui.button(label='1', style=discord.ButtonStyle.secondary, row=0)
    async def one(self, interaction, button):
        self.result += '1'
        await interaction.response.edit_message(content=self.result, view=self)

    # ... 추가 버튼 ...
    @discord.ui.button(label='=', style=discord.ButtonStyle.success, row=3)
    async def equals(self, interaction, button):
        try:
            value = eval(self.result)
            self.result = str(value)
        except Exception:
            self.result = '에러'
        await interaction.response.edit_message(content=self.result, view=self)
```

이처럼 버튼을 여러 행에 배치해 계산기 인터페이스를 구현할 수 있습니다. 복잡한 UI를 설계할 때는 각 행을 그룹으로 생각하고 배치를 계획하세요.

## 2. 인터랙션 체크와 사용자 제한

`View.interaction_check()` 메서드를 오버라이드하면 버튼 클릭 시 추가 검사를 수행할 수 있습니다. 예를 들어, 버튼을 생성한 사용자만 사용할 수 있도록 하거나, 특정 역할을 가진 사용자에게만 버튼 기능을 제공할 수 있습니다. 아래 예제는 명령어 호출자만 버튼을 사용할 수 있도록 제한하는 방법을 보여줍니다:

```python
class OwnerView(discord.ui.View):
    def __init__(self, owner: discord.User):
        super().__init__(timeout=60)
        self.owner = owner

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user != self.owner:
            await interaction.response.send_message('이 버튼을 사용할 권한이 없습니다.', ephemeral=True)
            return False
        return True

    @discord.ui.button(label='확인', style=discord.ButtonStyle.primary)
    async def confirm(self, interaction, button):
        await interaction.response.send_message('승인되었습니다!', delete_after=5)
        self.stop()

    @discord.ui.button(label='취소', style=discord.ButtonStyle.danger)
    async def cancel(self, interaction, button):
        await interaction.response.send_message('취소되었습니다.', delete_after=5)
        self.stop()
```

`self.stop()`은 뷰의 타임아웃을 즉시 종료하여 모든 버튼을 비활성화합니다. 권한 검사를 적극적으로 활용하면 버튼 악용을 방지할 수 있습니다.

## 3. 영구적 뷰 (Persistent View)

봇을 재시작한 이후에도 버튼을 유지하려면 영구적 뷰를 사용해야 합니다. 이를 위해서는 다음 조건을 충족해야 합니다:

1. 뷰의 `timeout`을 `None`으로 설정합니다.
2. 모든 버튼과 인터랙션 컴포넌트에 **고유한 `custom_id`**를 지정합니다.
3. 봇이 실행될 때 `bot.add_view()`로 뷰를 등록합니다.

```python
class RoleSelectionView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        # custom_id를 명시적으로 지정
        self.add_item(discord.ui.Button(label='환영 역할', style=discord.ButtonStyle.primary, custom_id='give_welcome_role'))
        self.add_item(discord.ui.Button(label='공지 역할', style=discord.ButtonStyle.secondary, custom_id='give_announce_role'))

    @discord.ui.button(label='환영 역할', style=discord.ButtonStyle.primary, custom_id='give_welcome_role')
    async def welcome_role(self, interaction, button):
        # 역할 부여 로직
        await interaction.response.send_message('환영 역할을 부여했습니다.', ephemeral=True)

    # ...

@bot.event
async def on_ready():
    bot.add_view(RoleSelectionView())  # 봇 시작 시 등록

```

Persistent view는 메시지가 오래 지속되는 규칙 역할 배정 메시지, 서버 규칙 확인 등에서 유용합니다. 각 버튼의 `custom_id`는 서버 재시작 후에도 동일해야 하며, 최대 100개의 persistent view를 등록할 수 있습니다.

## 4. 버튼 상태 변경과 동적 업데이트

버튼을 클릭한 후 비활성화하거나 다른 라벨/스타일로 변경할 수 있습니다. 예를 들어, 투표 시스템에서 사용자가 투표하면 버튼을 비활성화하여 중복 투표를 방지할 수 있습니다:

```python
class VoteView(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.yes_votes = 0
        self.no_votes = 0

    @discord.ui.button(label='찬성', style=discord.ButtonStyle.success)
    async def vote_yes(self, interaction, button):
        self.yes_votes += 1
        button.disabled = True
        await interaction.response.edit_message(content=f'찬성: {self.yes_votes}, 반대: {self.no_votes}', view=self)

    @discord.ui.button(label='반대', style=discord.ButtonStyle.danger)
    async def vote_no(self, interaction, button):
        self.no_votes += 1
        button.disabled = True
        await interaction.response.edit_message(content=f'찬성: {self.yes_votes}, 반대: {self.no_votes}', view=self)
```

이 예제는 버튼 상태를 즉시 업데이트하여 사용자가 여러 번 클릭할 수 없도록 합니다. 뷰와 버튼 상태를 적절히 변경하면 상호작용을 직관적으로 만들 수 있습니다.

이 장에서는 행 배치, 권한 검사, 영구적 뷰, 버튼 상태 변경 등 버튼의 고급 기능을 다뤘습니다. 다음 장에서는 선택 메뉴(select menu)를 사용해 복잡한 선택 인터페이스를 구현하는 방법을 살펴봅니다.



