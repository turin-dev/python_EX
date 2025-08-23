# 28장 – 리액션 이벤트와 역할 부여

리액션(이모지)을 이용하면 사용자가 특정 메시지에 반응할 때 자동으로 역할을 부여하거나 제거할 수 있습니다. 하지만 메시지가 캐시에 없을 수도 있기 때문에 `on_raw_reaction_add`와 `on_raw_reaction_remove` 이벤트를 사용하는 것이 안전합니다. 이 이벤트는 메시지 ID, 채널 ID, 사용자 ID, 이모지 정보를 포함한 페이로드를 제공합니다.

## 리액션 역할 구현

먼저 역할을 지정할 메시지를 전송하고, 사용자가 반응을 누르면 역할을 부여하는 이벤트 핸들러를 만듭니다. 예제에서는 특정 메시지 ID와 이모지를 매핑하여 해당 리액션을 추가한 사용자에게 역할을 부여합니다.

```python
from discord.ext import commands
import discord

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

ROLE_MESSAGE_ID = 123456789012345678  # 역할 부여를 위한 메시지 ID
EMOJI_TO_ROLE = {
    "🔴": 987654321098765432,  # 레드 역할 ID
    "🔵": 987654321098765433,  # 블루 역할 ID
}

@bot.event
async def on_raw_reaction_add(payload: discord.RawReactionActionEvent):
    if payload.message_id != ROLE_MESSAGE_ID:
        return
    guild = bot.get_guild(payload.guild_id)
    role_id = EMOJI_TO_ROLE.get(str(payload.emoji))
    if role_id is None:
        return
    role = guild.get_role(role_id)
    member = guild.get_member(payload.user_id)
    if role and member:
        await member.add_roles(role)
        print(f"{member.display_name}에게 {role.name} 역할 부여")

@bot.event
async def on_raw_reaction_remove(payload: discord.RawReactionActionEvent):
    if payload.message_id != ROLE_MESSAGE_ID:
        return
    guild = bot.get_guild(payload.guild_id)
    role_id = EMOJI_TO_ROLE.get(str(payload.emoji))
    member = guild.get_member(payload.user_id)
    if role_id and member:
        role = guild.get_role(role_id)
        await member.remove_roles(role)
```

이 코드를 사용하기 위해서는 `intents.reactions`와 `intents.members`를 활성화해야 하며, 봇 역할의 위치가 대상 역할보다 높아야 합니다. 또한 사용자가 리액션을 제거할 때 역할을 삭제하도록 `on_raw_reaction_remove` 이벤트도 구현해야 합니다.

## 캐시되지 않은 메시지 처리

`on_reaction_add` 이벤트는 메시지가 내부 캐시에 있어야 호출됩니다. 따라서 오래된 메시지나 봇이 시작되기 전에 전송된 메시지에 대한 리액션을 처리하려면 항상 `on_raw_reaction_add`와 `on_raw_reaction_remove`를 사용하세요. 페이로드에는 `guild_id`, `channel_id`, `message_id`, `user_id`, `emoji` 등 필요한 정보가 모두 포함되어 있습니다.

## 요약

리액션 역할을 구현하면 사용자가 원하는 역할을 자유롭게 선택할 수 있어 서버 관리가 편리해집니다. 캐시되지 않은 메시지도 처리할 수 있도록 raw 이벤트를 사용하고, 이모지와 역할 ID를 매핑하여 역할을 부여하거나 제거하세요. `discord.Intents`에서 `reactions`와 `members` 권한을 활성화하는 것을 잊지 마세요【666664033931420†L32-L45】.

