# 41장 – 버튼 스타일과 상태 관리

앞선 장에서는 기본 버튼을 생성하고 콜백을 구현하는 방법을 살펴봤습니다. 이번에는 버튼의 **스타일(style)** 과 **상태(state)** 를 다양하게 지정하는 방법을 알아봅니다. 버튼은 `discord.ui.Button` 클래스에서 `style`, `emoji`, `custom_id`, `row`, `disabled` 등을 설정하여 다채로운 인터페이스를 만들 수 있습니다【716329102970593†L5969-L6031】.

## 스타일과 라벨

버튼의 색상과 느낌은 `ButtonStyle` 열거형으로 지정합니다. 주요 스타일에는 `primary`(파란색), `secondary`(회색), `success`(초록), `danger`(빨강)가 있으며, `link` 스타일을 사용하면 버튼이 URL을 열 수 있습니다. 라벨과 이모지를 함께 사용하여 버튼을 직관적으로 만들 수 있습니다.

```python
from discord.ui import Button, View

class ColorView(View):
    def __init__(self):
        super().__init__()
        self.add_item(Button(label="확인", style=discord.ButtonStyle.primary))
        self.add_item(Button(label="취소", style=discord.ButtonStyle.danger))
        self.add_item(Button(label="도움", style=discord.ButtonStyle.secondary, emoji="❔"))
```

링크 버튼은 `url` 매개변수로 지정하며, 콜백 함수가 필요 없습니다. 사용자가 클릭하면 지정된 웹 페이지가 열립니다.

## 버튼 상태 변경과 비활성화

버튼은 상호작용 후 비활성화(disabled)할 수 있습니다. 예를 들어 투표 시스템에서 사용자가 선택한 버튼을 끄고, 결과를 표시하는 데 활용할 수 있습니다.

```python
class VoteView(View):
    def __init__(self):
        super().__init__()
        self.voted = False

    @discord.ui.button(label="찬성", style=discord.ButtonStyle.success)
    async def approve(self, interaction: discord.Interaction, button: Button):
        if self.voted:
            return
        button.disabled = True
        self.voted = True
        await interaction.response.edit_message(content="찬성을 선택했습니다.", view=self)

    @discord.ui.button(label="반대", style=discord.ButtonStyle.danger)
    async def disapprove(self, interaction: discord.Interaction, button: Button):
        if self.voted:
            return
        button.disabled = True
        self.voted = True
        await interaction.response.edit_message(content="반대를 선택했습니다.", view=self)
```

버튼을 비활성화하면 사용자가 다시 클릭할 수 없으며, 메시지를 갱신하여 변경 사항을 반영해야 합니다. 또한 `row` 매개변수로 버튼의 행을 지정하여 메시지 레이아웃을 관리할 수 있습니다. 한 행에 최대 5개의 요소를 배치할 수 있으며, 5행까지 지원합니다【716329102970593†L5969-L6031】.

## 요약

버튼 스타일과 상태를 조정하면 사용자 인터페이스를 보다 직관적이고 안전하게 만들 수 있습니다. 스타일 열거형으로 색상과 용도를 구분하고, 상황에 따라 버튼을 비활성화하여 중복 입력을 방지하세요. 행(row)과 이모지를 활용해 레이아웃과 가독성을 향상시킬 수 있습니다.

