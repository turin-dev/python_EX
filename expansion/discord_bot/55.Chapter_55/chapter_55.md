# 리액션 역할과 버튼 역할

서버에서 특정 역할을 사용자가 스스로 선택하도록 허용하고 싶을 때 **리액션 역할**과 **버튼 역할**을 활용할 수 있습니다. 리액션 역할은 사용자에게 이모지를 눌러 역할을 선택하도록 하는 전통적인 방법이고, 버튼 역할은 `discord.ui.Button`을 이용해 더 직관적인 UI를 제공합니다.

## 리액션 역할 구현

리액션 역할을 구현하려면 `on_raw_reaction_add`와 `on_raw_reaction_remove` 이벤트를 이용해 사용자의 리액션 추가/삭제를 감지하고, 그에 따라 역할을 부여하거나 제거합니다. `on_raw_` 이벤트는 메시지 캐시와 관계없이 동작하므로 신뢰할 수 있습니다. 아래 예제는 한 메시지에 특정 이모지를 누르면 역할을 부여하는 패턴입니다.

```python
import discord
from discord.ext import commands

ROLE_MESSAGE_ID = 123456789012345678  # 역할 선택 메시지 ID
EMOJI_TO_ROLE = {"✅": 987654321098765432}  # 이모지: 역할 ID 매핑

class ReactionRoleCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
        if payload.message_id != ROLE_MESSAGE_ID:
            return
        emoji = str(payload.emoji)
        if emoji not in EMOJI_TO_ROLE:
            return
        guild = self.bot.get_guild(payload.guild_id)
        member = guild.get_member(payload.user_id)
        role = guild.get_role(EMOJI_TO_ROLE[emoji])
        if member and role:
            await member.add_roles(role, reason="리액션 역할 부여")

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload: discord.RawReactionActionEvent):
        if payload.message_id != ROLE_MESSAGE_ID:
            return
        emoji = str(payload.emoji)
        if emoji not in EMOJI_TO_ROLE:
            return
        guild = self.bot.get_guild(payload.guild_id)
        member = guild.get_member(payload.user_id)
        role = guild.get_role(EMOJI_TO_ROLE[emoji])
        if member and role:
            await member.remove_roles(role, reason="리액션 역할 제거")
```

리액션 역할을 사용하면 메시지 하나로 여러 역할을 선택할 수 있지만, 단점으로는 이모지 목록이 많아지면 복잡해지며 모바일 사용자가 실수로 다른 역할을 선택할 수 있습니다.

## 버튼을 이용한 역할 부여

`discord.ui.Button`을 이용하면 사용자 경험을 향상시키고, 버튼 클릭 후 역할이 즉시 적용됨을 명확히 보여줄 수 있습니다. 버튼에는 `custom_id`를 지정해 콜백에서 어떤 버튼인지 식별할 수 있습니다【716329102970593†L5969-L6031】. 다음은 두 개의 역할을 선택할 수 있는 버튼 뷰 예제입니다:

```python
class RoleButtonView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)  # 지속 뷰로 설정하려면 timeout을 None으로 설정

    @discord.ui.button(label="개발자", custom_id="role_dev", style=discord.ButtonStyle.primary)
    async def dev_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        role = interaction.guild.get_role(DEV_ROLE_ID)
        if role:
            await interaction.user.add_roles(role)
            await interaction.response.send_message("개발자 역할이 부여되었습니다.", ephemeral=True)

    @discord.ui.button(label="디자이너", custom_id="role_designer", style=discord.ButtonStyle.primary)
    async def designer_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        role = interaction.guild.get_role(DESIGNER_ROLE_ID)
        if role:
            await interaction.user.add_roles(role)
            await interaction.response.send_message("디자이너 역할이 부여되었습니다.", ephemeral=True)
```

위 뷰를 메시지와 함께 전송할 때는 `await channel.send("원하는 역할을 선택하세요", view=RoleButtonView())`처럼 사용합니다. 버튼은 각자의 `custom_id`로 식별되며, 뷰를 지속적으로 사용하려면 `timeout=None`으로 설정하고 봇 시작 시 `bot.add_view(RoleButtonView())`를 호출해야 합니다【716329102970593†L4889-L4924】.

## 참고 사항

- 리액션 역할을 사용할 때는 봇이 `add_reactions`와 `manage_roles` 권한을 갖고 있어야 합니다.
- 버튼 역할은 UI가 직관적이지만, 각 버튼에 대해 별도의 콜백을 작성해야 합니다. 역할 갯수가 많다면 `discord.ui.Select`를 고려해 볼 수 있습니다.
- 역할을 마음대로 부여하도록 허용하는 것은 보안 위험이 될 수 있으므로, 민감한 권한을 가진 역할에는 관리자의 승인을 요구하는 것이 좋습니다.

역할 선택 인터페이스를 적절히 구성하면 사용자가 자발적으로 역할을 관리할 수 있어 서버 운영자의 부담을 줄일 수 있습니다.

\[뷰와 버튼의 세부 속성 설명\]【716329102970593†L5969-L6031】【716329102970593†L4889-L4924】

