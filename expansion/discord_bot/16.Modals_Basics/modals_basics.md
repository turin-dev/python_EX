# 모달 기본

**모달(modal)**은 Discord에서 사용자로부터 여러 줄의 입력을 받을 수 있는 팝업 창입니다. 슬래시 커맨드나 버튼을 통해 호출되며, 사용자가 정보를 입력한 후 제출하면 봇이 결과를 처리할 수 있습니다. 폼 형태의 입력을 요구할 때 유용하며, 최대 5개의 입력 필드를 포함할 수 있습니다.

모달을 정의하려면 `discord.ui.Modal`을 상속하는 클래스를 생성하고, 클래스 속성으로 `discord.ui.TextInput` 필드를 선언합니다. 그 후 `on_submit()` 메서드를 구현하여 사용자가 입력한 값을 처리합니다. 모달은 슬래시 커맨드 또는 버튼 콜백에서 `interaction.response.send_modal()`을 호출하여 전송할 수 있습니다.

## 1. 모달 클래스 정의

다음 예제는 피드백을 받기 위한 모달을 정의하는 방법을 보여줍니다. `TextInput`은 두 가지 스타일(`short` 단일 라인, `paragraph` 다중 라인)을 지원하며, `label`, `placeholder`, `default`, `min_length`, `max_length`, `required` 등의 속성을 설정할 수 있습니다:

```python
import discord

class FeedbackModal(discord.ui.Modal, title='피드백 제출'):
    name = discord.ui.TextInput(label='닉네임', placeholder='별명을 입력하세요', required=True, max_length=32)
    feedback = discord.ui.TextInput(label='피드백 내용', style=discord.TextStyle.paragraph, placeholder='어떤 점이 좋았나요?', max_length=500)

    async def on_submit(self, interaction: discord.Interaction):
        # 입력값 접근: self.name.value, self.feedback.value
        await interaction.response.send_message('피드백을 제출해 주셔서 감사합니다!', ephemeral=True)
        # 여기서 데이터베이스에 저장하거나 개발자 채널로 전송할 수 있습니다

    async def on_error(self, interaction: discord.Interaction, error: Exception) -> None:
        # 오류 처리: 모달 처리 중 발생한 예외를 로그에 남기고 사용자에게 안내
        await interaction.response.send_message('오류가 발생했습니다. 다시 시도해 주세요.', ephemeral=True)
        # raise error  # 필요에 따라 예외를 다시 발생시켜 상위 핸들러로 전달
```

`on_submit` 메서드에서는 `self.<field>.value`로 사용자가 입력한 내용을 조회할 수 있습니다. `on_error` 메서드는 모달 처리 중 발생한 예외를 처리하며, 오버라이드하지 않으면 예외가 그대로 전파됩니다.

## 2. 모달 보내기

모달은 `interaction.response.send_modal()`로 전송할 수 있습니다. 이 메서드는 슬래시 커맨드 핸들러나 버튼 콜백에서 호출해야 하며, 이미 응답을 보냈거나 지연 응답을 예약한 상태에서는 사용할 수 없습니다. 예를 들어, 슬래시 커맨드에서 피드백 모달을 띄우는 방법은 다음과 같습니다:

```python
@bot.tree.command(name='feedback', description='피드백 제출 폼')
async def feedback_command(interaction: discord.Interaction):
    await interaction.response.send_modal(FeedbackModal())
```

또는 버튼 콜백에서도 사용할 수 있습니다:

```python
class FeedbackButton(discord.ui.Button):
    def __init__(self):
        super().__init__(label='피드백 작성', style=discord.ButtonStyle.primary)

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_modal(FeedbackModal())

view = discord.ui.View()
view.add_item(FeedbackButton())
await channel.send('피드백을 남겨주세요:', view=view)
```

## 3. 주의 사항과 제한

- 하나의 모달에는 최대 5개의 `TextInput` 필드를 포함할 수 있습니다.
- 각 입력 필드에는 고유한 `custom_id`가 자동 생성되지만, 필요한 경우 `custom_id`를 명시적으로 지정해 서버 재시작 후에도 모달 데이터를 구분할 수 있습니다.
- 모달은 두 번째 응답을 허용하지 않으므로, 이미 `interaction.response`가 사용된 상태에서는 모달을 전송할 수 없습니다. 이러한 경우에는 `interaction.followup.send()`를 사용하여 추가 메시지를 보내야 합니다.

모달을 적절히 활용하면 사용자가 여러 줄의 입력을 편리하게 제공할 수 있습니다. 다음 장에서는 버튼과 같은 UI 컴포넌트를 이용해 상호작용을 확장하는 방법을 설명합니다.



