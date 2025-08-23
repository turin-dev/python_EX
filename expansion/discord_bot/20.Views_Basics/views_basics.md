# 뷰 기본

**View**는 Discord UI 컴포넌트를 담는 컨테이너로, 버튼, 선택 메뉴, 모달 트리거 등 여러 요소를 하나의 인터페이스로 묶어줍니다. 뷰는 메시지와 함께 전송되며, 사용자가 요소와 상호작용할 수 있도록 관리합니다【716329102970593†L4889-L4924】. 이 장에서는 뷰의 구조, 속성, 이벤트 후킹과 동적 조작에 대해 살펴봅니다.

## 1. 뷰 생성과 사용

뷰를 사용하려면 `discord.ui.View`를 서브클래싱하거나 인스턴스를 생성한 뒤 요소를 수동으로 추가할 수 있습니다. 서브클래싱 방법은 클래스 내부에 버튼이나 선택 메뉴를 데코레이터로 선언하고, `interaction_check`나 `on_timeout` 등의 메서드를 오버라이드해 동작을 커스터마이즈할 수 있습니다:

```python
class ConfirmView(discord.ui.View):
    def __init__(self, *, timeout: float = 30):
        super().__init__(timeout=timeout)
        self.value = None

    @discord.ui.button(label='확인', style=discord.ButtonStyle.success)
    async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.value = True
        await interaction.response.defer()  # 응답 연기
        self.stop()  # 뷰 종료

    @discord.ui.button(label='취소', style=discord.ButtonStyle.danger)
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.value = False
        await interaction.response.defer()
        self.stop()

    async def on_timeout(self) -> None:
        # 타임아웃 시 호출: 아무런 선택 없이 종료됨
        self.value = False

view = ConfirmView(timeout=60)
await ctx.send('계속 진행하시겠습니까?', view=view)
await view.wait()  # 사용자의 선택을 기다림
if view.value:
    await ctx.send('계속 진행합니다.')
else:
    await ctx.send('작업이 취소되었습니다.')
```

`view.wait()`은 뷰가 종료될 때까지 비동기적으로 대기합니다. 타임아웃이 지나거나 `self.stop()`이 호출되면 뷰가 비활성화되고, 모든 버튼이 더 이상 클릭되지 않습니다.

## 2. 속성과 메서드

- **timeout**: 뷰가 활성 상태를 유지하는 시간(초)입니다. 기본값은 180초이며, `None`으로 설정하면 영구적 뷰가 됩니다.
- **children**: 뷰에 포함된 UI 요소(버튼, 선택 메뉴 등)의 리스트입니다. 뷰가 생성된 후 `add_item(item)`으로 요소를 추가하고, `remove_item(item)`으로 제거할 수 있습니다.
- **interaction_check(self, interaction)**: 사용자가 상호작용하기 전에 호출되며, 반환값이 `False`이면 상호작용이 거부됩니다. 버튼 고급 사용에서 설명한 것처럼 권한 체크에 활용할 수 있습니다.
- **on_timeout(self)**: 뷰의 타임아웃이 발생했을 때 호출됩니다. 여기서 메시지를 수정하거나 후속 조치를 취할 수 있습니다.
- **on_error(self, error, item, interaction)**: 뷰 또는 컴포넌트에서 예외가 발생했을 때 호출되어 오류를 처리합니다.

## 3. 동적 뷰 조작

뷰는 실행 중에도 동적으로 UI 요소를 추가하거나 제거할 수 있습니다. 예를 들어, 투표가 종료되면 버튼을 삭제하거나 비활성화할 수 있습니다. 다음 예제는 동적으로 버튼을 추가하는 방법을 보여줍니다:

```python
view = discord.ui.View()
view.add_item(discord.ui.Button(label='새 버튼', style=discord.ButtonStyle.primary))
await message.edit(view=view)
```

요소를 수정하려면 `view.children`에서 특정 항목을 찾아 속성을 변경한 후, 메시지를 업데이트해야 합니다. 뷰 내부의 상태를 변경한 경우 `interaction.response.edit_message(view=self)`를 호출하여 변경 사항을 클라이언트에 반영합니다.

이번 장에서는 뷰의 기본 개념과 필수 메서드를 살펴보았습니다. 뷰를 제대로 이해하면 여러 UI 컴포넌트를 조합하여 복잡한 인터랙션을 만들 수 있습니다. 다음 장부터는 추가적인 주제들을 다루는 확장 섹션으로 넘어갑니다.



