# 42장 – 지속적인 뷰와 상태 보존

앞선 장에서 우리는 버튼과 셀렉트 메뉴가 포함된 뷰를 만들고 콜백을 처리하는 방법을 배웠습니다. 그러나 봇을 재시작하면 이러한 인터페이스가 더 이상 동작하지 않는다는 점이 문제였습니다. **지속적인(Persistent) 뷰**를 사용하면 봇을 재배포하거나 코드가 변경된 후에도 인터랙션 UI가 계속 작동합니다. 이 장에서는 지속적인 뷰를 만드는 방법과 상태를 저장하는 패턴을 알아봅니다.

## 지속적인 뷰의 조건

`discord.py` 2.x에서는 뷰가 다음 조건을 만족할 때 **persistent**로 간주합니다:

* 뷰의 `timeout` 속성이 **`None`** 이어야 합니다.
* 모든 UI 컴포넌트(Button, Select 등)에 **`custom_id`** 값이 명시되어 있어야 합니다.

공식 문서에서도 "A persistent view has all their components with a set `custom_id` and a timeout set to `None`"라고 설명합니다【716329102970593†L5057-L5063】. 컴포넌트는 고유한 `custom_id`를 통해 상호작용 요청을 매핑할 수 있고, `timeout`이 없으므로 봇 재시작 후에도 만료되지 않습니다.

지속적인 뷰를 사용하려면 봇이 시작될 때 `Bot.add_view()`로 뷰를 **등록**해야 합니다. 예를 들어, `on_ready` 또는 `setup_hook`에서 `bot.add_view(view_instance)`를 호출하여 런타임 동안 해당 뷰를 계속 수신 대기하도록 설정합니다.

## 예제: 역할 선택 뷰

아래 예제는 특정 역할을 부여하거나 제거할 수 있는 두 개의 버튼을 포함한 지속적인 뷰입니다. 각 버튼에는 고유한 `custom_id`가 설정되어 있으며, 뷰의 `timeout`은 `None`으로 설정되어 있습니다. 봇이 시작될 때 뷰를 등록하기 때문에 재시작 후에도 버튼이 작동합니다.

```python
import discord
from discord.ext import commands


class RoleView(discord.ui.View):
    """지속적인 역할 관리 뷰."""

    def __init__(self, role: discord.Role):
        super().__init__(timeout=None)  # persistent
        self.role = role

        # 역할 부여 버튼
        join_button = discord.ui.Button(
            label="역할 부여",
            style=discord.ButtonStyle.success,
            custom_id="role_join"
        )
        join_button.callback = self.join_callback
        self.add_item(join_button)

        # 역할 제거 버튼
        leave_button = discord.ui.Button(
            label="역할 제거",
            style=discord.ButtonStyle.danger,
            custom_id="role_leave"
        )
        leave_button.callback = self.leave_callback
        self.add_item(leave_button)

    async def join_callback(self, interaction: discord.Interaction):
        member = interaction.user
        if self.role not in member.roles:
            await member.add_roles(self.role)
            await interaction.response.send_message(
                f"{self.role.name} 역할을 부여했습니다.",
                ephemeral=True
            )
        else:
            await interaction.response.send_message(
                f"이미 {self.role.name} 역할이 있습니다.",
                ephemeral=True
            )

    async def leave_callback(self, interaction: discord.Interaction):
        member = interaction.user
        if self.role in member.roles:
            await member.remove_roles(self.role)
            await interaction.response.send_message(
                f"{self.role.name} 역할을 제거했습니다.",
                ephemeral=True
            )
        else:
            await interaction.response.send_message(
                f"{self.role.name} 역할이 없습니다.",
                ephemeral=True
            )


async def setup(bot: commands.Bot):
    # 봇이 시작될 때 지속적인 뷰를 등록합니다. role_id는 실제 역할 ID로 바꾸세요.
    async def on_ready_once():
        guild = bot.guilds[0]  # 예시: 첫 번째 길드
        role = guild.get_role(123456789012345678)  # 실제 역할 ID를 입력하세요
        bot.add_view(RoleView(role))
    # setup_hook에서 호출할 수 있도록 래핑합니다.
    bot.add_listener(on_ready_once, name="on_ready")

```

위 예제에서는 `custom_id`를 지정한 버튼을 수동으로 생성하고 `callback` 속성에 메서드를 할당했습니다. 봇이 재시작되더라도, 고유 `custom_id`를 통해 콜백이 매핑되기 때문에 버튼이 그대로 작동합니다.

## 상태 보존을 위한 저장소 사용

지속적인 뷰는 UI만 유지할 뿐, 버튼 클릭 여부나 기타 상태는 메모리에 저장됩니다. 따라서 봇 재시작 시 상태가 초기화됩니다. 상태를 유지하려면 다음과 같은 전략을 사용할 수 있습니다:

* **데이터베이스**: SQLite 또는 외부 데이터베이스에 사용자의 선택이나 투표 결과를 저장합니다. 버튼 콜백에서 DB를 갱신하고, 메시지를 업데이트할 때 DB 값을 읽어옵니다.
* **파일 저장**: 간단한 경우 JSON 파일이나 YAML 파일에 상태를 기록할 수 있습니다. 다만 동시성 문제를 주의해야 합니다.
* **캐시**: 휘발성 상태는 `bot` 인스턴스나 싱글톤 클래스에 저장할 수 있으며, 주기적으로 디스크에 덤프하거나 안전하지 않은 정보를 저장하지 않도록 합니다.

예를 들어 위 역할 부여 뷰에서 사용자가 이미 버튼을 클릭했는지를 데이터베이스에 기록하면 봇을 재시작해도 중복 역할 부여를 방지할 수 있습니다.

## 요약

지속적인 뷰는 봇 재시작 이후에도 상호작용 컴포넌트를 유지할 수 있는 강력한 도구입니다. `timeout=None`으로 설정하고 각 컴포넌트에 `custom_id`를 지정해야 하며, 봇 초기화 시 `bot.add_view()`를 호출하여 등록해야 합니다【716329102970593†L5057-L5063】. 상태까지 영구히 저장하려면 데이터베이스나 파일을 활용해 버튼 클릭 여부를 저장하고 복원하는 것이 좋습니다.