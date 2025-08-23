# 45장 – 고급 모달 사용법

모달(modal)은 사용자가 여러 입력을 채울 수 있는 팝업 창입니다. 간단한 피드백 폼부터 복잡한 신청 양식까지 다양한 상황에서 활용할 수 있습니다. 이번 장에서는 모달의 구조, 입력 필드 설정, 검증 및 오류 처리 방법을 자세히 살펴봅니다.

## Modal 클래스와 매개변수

모달은 `discord.ui.Modal`을 상속하여 정의합니다. 문서에 따르면 모달 생성자는 `title`, `timeout`, `custom_id`를 인자로 받습니다【716329102970593†L5401-L5460】. 주요 속성은 다음과 같습니다:

* **title** – 모달 창 상단에 표시되는 제목입니다. 최대 45자까지 지정할 수 있습니다【716329102970593†L5450-L5454】.
* **timeout** – 마지막 상호작용 이후 몇 초 동안 모달이 열려 있을지를 지정합니다. `None`으로 설정하면 제한이 없으나, 모달은 메시지 기반 인터랙션이 아니기 때문에 지속적이지 않습니다【716329102970593†L5454-L5456】.
* **custom_id** – 상호작용 시 전달되는 모달의 ID입니다. 지정하지 않으면 자동 생성되며 100자까지 사용할 수 있습니다【716329102970593†L5458-L5460】.
* **children** – 모달에 포함된 입력 필드를 나타내는 속성입니다. 최대 5개의 `TextInput`을 추가할 수 있습니다【716329102970593†L5450-L5458】.

모달은 뷰와 달리 지속되지 않으며, 제출되면 바로 사라집니다. 따라서 재사용하려면 매번 새 인스턴스를 생성해야 합니다.

## 텍스트 입력 필드 설정

`discord.ui.TextInput` 클래스를 사용해 입력 필드를 정의합니다. 주요 매개변수는:

* **label** – 입력란 위에 표시되는 라벨.
* **style** – `discord.TextStyle.short` 또는 `discord.TextStyle.paragraph` 값을 지정해 한 줄 입력인지 여러 줄 입력인지 결정합니다.
* **placeholder** – 사용자가 아무 것도 입력하지 않았을 때 표시되는 안내 문구.
* **default** – 기본값을 미리 입력합니다.
* **required** – `True`이면 비워둘 수 없습니다.
* **min_length** / **max_length** – 입력 가능한 최소/최대 글자 수를 제한합니다.

입력 필드는 클래스 속성으로 선언하거나 `__init__()`에서 동적으로 생성할 수 있습니다. 필드 정의 순서가 모달에 표시되는 순서입니다.

## 예제: 피드백 모달 구현

다음 예제는 세 개의 입력 필드를 포함한 피드백 폼을 구현합니다. 사용자가 이름, 평점, 의견을 입력하면 서버에 메시지를 기록합니다. 평점은 1~5 범위로 제한되어 있으며, 검증에 실패하면 오류 메시지를 반환합니다.

```python
import discord
from discord import ui


class FeedbackModal(ui.Modal, title="피드백 제출"):
    name = ui.TextInput(label="이름", placeholder="닉네임 또는 실명", max_length=32)
    rating = ui.TextInput(label="평점 (1~5)", placeholder="숫자로 입력", max_length=1)
    comment = ui.TextInput(label="의견", style=discord.TextStyle.paragraph, required=False, max_length=500)

    async def on_submit(self, interaction: discord.Interaction) -> None:
        # 평점 검증
        try:
            score = int(self.rating.value)
            if not 1 <= score <= 5:
                raise ValueError
        except ValueError:
            await interaction.response.send_message("평점은 1에서 5 사이의 숫자여야 합니다.",
                                                  allowed_mentions=discord.AllowedMentions.none(),
                                                  ephemeral=True)
            return

        # 피드백 처리: 데이터베이스 저장, 로그 작성 등
        await interaction.response.send_message(
            f"{self.name}님의 피드백이 접수되었습니다. 감사합니다!", 
            allowed_mentions=discord.AllowedMentions.none(),
            epicms=True
        )

    async def on_error(self, interaction: discord.Interaction, error: Exception) -> None:
        # on_submit에서 예외가 발생하면 호출됩니다.
        await interaction.response.send_message(
            "모달 처리 중 오류가 발생했습니다.",
            allowed_mentions=discord.AllowedMentions.none(),
            ephemeral=True
        )


async def setup(bot: discord.Client) -> None:
    @bot.event
    async def on_ready() -> None:
        print("모달 테스트 준비 완료")

    @bot.tree.command(name="피드백", description="피드백 폼을 표시합니다")
    async def feedback_cmd(interaction: discord.Interaction):
        await interaction.response.send_modal(FeedbackModal())
```

이 예제에서 모달 클래스의 필드는 클래스 변수로 선언되어 있으며, 제출 시 `on_submit` 메서드에서 검증을 수행합니다. 오류 발생 시 `on_error`가 호출되어 사용자에게 메시지를 전달합니다. 모달은 지속적이지 않기 때문에 매번 새 인스턴스를 생성해야 합니다.

## 모달의 제한 사항

* 한 모달에는 최대 5개의 입력 필드를 사용할 수 있습니다.
* 각 입력은 최대 4000자의 텍스트를 받을 수 있지만, 모달 전체의 길이는 제한될 수 있습니다.
* 모달은 메시지나 버튼과 달리 `timeout` 후에 자동으로 소멸되므로, 다시 열려면 명령 또는 버튼에서 새로 전송해야 합니다.

## 요약

모달은 사용자에게 여러 입력을 받기 위한 강력한 도구이며, 각 입력 필드는 `label`, `style`, `placeholder`, `default`, `required` 등의 속성을 통해 세밀하게 제어할 수 있습니다. 모달은 `title`(최대 45자), `timeout`, `custom_id`를 매개변수로 가지며, 입력 필드는 최대 5개까지 추가할 수 있습니다【716329102970593†L5401-L5460】. 제출된 데이터는 `on_submit` 메서드에서 검증 및 처리하고, 오류가 발생하면 `on_error`를 통해 사용자에게 안내해야 합니다.