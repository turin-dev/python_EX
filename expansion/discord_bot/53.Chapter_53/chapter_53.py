"""자동 모더레이션과 필터링 예제.

이 모듈에는 욕설 필터링을 수행하는 코그와 AutoMod 규칙을
생성하는 함수가 포함되어 있습니다. 필터링 로직은 단순한 문자열
포함 여부를 기준으로 하지만, 실제 환경에서는 정규식이나 외부
블랙리스트를 활용해 좀 더 정교하게 구현할 수 있습니다.
"""

import discord
from discord.ext import commands


class ModerationCog(commands.Cog):
    """금칙어를 탐지하여 메시지를 삭제하고 경고하는 코그."""

    def __init__(self, bot: commands.Bot, banned_words: set[str], mute_role_id: int | None = None) -> None:
        self.bot = bot
        self.banned_words = {word.lower() for word in banned_words}
        self.warn_counts: dict[int, int] = {}
        self.mute_role_id = mute_role_id

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message) -> None:
        if message.author.bot:
            return
        content = message.content.lower()
        if any(word in content for word in self.banned_words):
            # 메시지 삭제 및 경고 전송
            await message.delete()
            uid = message.author.id
            self.warn_counts[uid] = self.warn_counts.get(uid, 0) + 1
            await message.channel.send(
                f"{message.author.mention} 경고! 금칙어 사용 {self.warn_counts[uid]}회.",
                delete_after=5
            )
            # 누적 경고가 3회 이상이면 뮤트 역할 부여
            if self.mute_role_id and self.warn_counts[uid] >= 3:
                role = message.guild.get_role(self.mute_role_id)
                if role:
                    await message.author.add_roles(role, reason="금칙어 반복")


async def setup_automod_rule(guild: discord.Guild) -> None:
    """길드에 AutoMod 규칙을 생성합니다. 이미 존재하면 아무것도 하지 않습니다."""
    for rule in guild.auto_moderation_rules:
        if rule.name == "금칙어 필터":
            return
    await guild.create_auto_moderation_rule(
        name="금칙어 필터",
        event_type=discord.AutoModerationEventType.message_send,
        trigger_type=discord.AutoModerationTriggerType.keyword,
        trigger_metadata=discord.AutoModerationTriggerMetadata(
            keyword_filter=["욕설", "비방"]
        ),
        actions=[discord.AutoModerationAction(
            type=discord.AutoModerationActionType.block_message,
            metadata=discord.AutoModerationActionMetadata(custom_message="금칙어가 포함되어 있습니다.")
        )],
    )

