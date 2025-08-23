"""리액션 역할 예제.

지정한 메시지에 특정 이모지를 추가하면 대응하는 역할을 부여하고,
리액션을 제거하면 역할을 제거합니다. 캐시되지 않은 메시지를 처리하기 위해
raw 이벤트를 사용합니다.
"""

import discord
from discord.ext import commands


ROLE_MESSAGE_ID = 123456789012345678  # 실제 메시지 ID로 변경하세요
EMOJI_TO_ROLE = {
    "🔴": 987654321098765432,  # 각 이모지에 대응하는 역할 ID를 입력
    "🔵": 987654321098765433,
}


bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())


@bot.event
async def on_raw_reaction_add(payload: discord.RawReactionActionEvent) -> None:
    if payload.message_id != ROLE_MESSAGE_ID:
        return
    guild = bot.get_guild(payload.guild_id)
    role_id = EMOJI_TO_ROLE.get(str(payload.emoji))
    if role_id is None or guild is None:
        return
    role = guild.get_role(role_id)
    member = guild.get_member(payload.user_id)
    if role and member:
        await member.add_roles(role)
        print(f"{member.display_name}에게 {role.name} 역할 부여")


@bot.event
async def on_raw_reaction_remove(payload: discord.RawReactionActionEvent) -> None:
    if payload.message_id != ROLE_MESSAGE_ID:
        return
    guild = bot.get_guild(payload.guild_id)
    role_id = EMOJI_TO_ROLE.get(str(payload.emoji))
    member = guild.get_member(payload.user_id) if guild else None
    if role_id and member:
        role = guild.get_role(role_id)
        await member.remove_roles(role)


if __name__ == "__main__":
    # bot.run("YOUR_TOKEN")
    pass