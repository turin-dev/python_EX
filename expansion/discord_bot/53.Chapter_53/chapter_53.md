# 자동 모더레이션과 필터링

커뮤니티가 커질수록 스팸이나 부적절한 콘텐츠를 막는 일이 중요해집니다. 디스코드에는 **자동 모더레이션(AutoMod)** 기능이 있어 금칙어, 필터링 규칙을 서버 설정에서 관리할 수 있습니다. `discord.py` 2.1 이후에서는 `Guild.create_auto_moderation_rule()` 메서드를 통해 봇이 직접 규칙을 등록할 수 있으며, 봇 자체적으로도 메시지를 감시해 불필요한 내용을 처리할 수 있습니다.

## 금칙어 필터 구현

가장 간단한 필터는 특정 단어가 포함된 메시지를 삭제하고 경고를 남기는 방식입니다. `on_message` 이벤트에서 메시지를 검사하고, 발견 시 삭제합니다. 아래 예제에서는 금칙어 목록과 경고 카운트를 저장하여 반복 위반 시 조치를 강화하는 패턴을 보여줍니다.

```python
from discord.ext import commands

class ModerationCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.banned_words = {"바보", "욕설"}
        self.warn_counts: dict[int, int] = {}

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return
        lowered = message.content.lower()
        if any(word in lowered for word in self.banned_words):
            await message.delete()
            user_id = message.author.id
            self.warn_counts[user_id] = self.warn_counts.get(user_id, 0) + 1
            await message.channel.send(
                f"{message.author.mention} 경고! 금칙어를 사용했습니다. "
                f"누적 경고: {self.warn_counts[user_id]}회",
                delete_after=5
            )
            if self.warn_counts[user_id] >= 3:
                mute_role = message.guild.get_role(MUTE_ROLE_ID)
                if mute_role:
                    await message.author.add_roles(mute_role, reason="금칙어 반복")
            return
```

위와 같이 직접 필터를 구현할 경우 **권한 처리**와 **명예훼손 등 법적 책임**을 고려해야 합니다. 명확한 이용 규칙을 공지하고, 지나친 검열을 피하는 것이 좋습니다.

## 자동 모더레이션 규칙 등록

디스코드가 제공하는 AutoMod는 금칙어, 스팸 멘션, 토큰/링크 탐지 규칙을 서버 설정에서 관리합니다. 봇은 다음과 같이 금칙어 규칙을 프로그래밍적으로 생성할 수 있습니다. 이 기능을 사용하려면 서버에서 AutoMod가 활성화되어 있어야 합니다.

```python
async def setup_automod_rule(guild: discord.Guild):
    # 기존 규칙이 있는지 확인하고 중복 생성 방지
    for rule in guild.auto_moderation_rules:
        if rule.name == "금칙어 필터":
            return
    await guild.create_auto_moderation_rule(
        name="금칙어 필터",
        event_type=discord.AutoModerationEventType.message_send,
        trigger_type=discord.AutoModerationTriggerType.keyword,
        trigger_metadata=discord.AutoModerationTriggerMetadata(keyword_filter=["욕설", "비방"]),
        actions=[discord.AutoModerationAction(
            type=discord.AutoModerationActionType.block_message,
            metadata=discord.AutoModerationActionMetadata(custom_message="금칙어가 포함되어 있습니다.")
        )]
    )
```

AutoMod 규칙은 서버 관리자가 활성화/비활성화할 수 있으며, 위반 항목이 발견되면 자동으로 메시지가 차단됩니다. 특정 사용자 또는 역할을 필터 대상에서 제외할 수도 있습니다. 이러한 기능을 적절히 활용하면 봇 코드의 복잡도를 줄일 수 있습니다.

## 요약

자동 모더레이션은 서버의 질서를 유지하는 데 필수적입니다. 디스코드가 제공하는 AutoMod 규칙을 활용하고, 봇 코드로 세밀한 필터를 구현하여 스팸과 욕설을 줄일 수 있습니다. 단, 과도한 필터링은 사용자 경험을 해칠 수 있으므로 규칙을 명확히 안내하고 예외 처리를 마련해야 합니다.

\[루프와 타이머 관련 참고\]【230406618874054†L160-L210】

