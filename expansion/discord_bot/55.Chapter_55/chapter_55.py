"""리액션 역할과 버튼 역할 예제.

이 모듈은 두 가지 역할 선택 방식을 구현합니다.

1. ReactionRoleCog: 특정 메시지의 리액션 추가/삭제를 감지하여 역할을 부여/제거합니다.
2. RoleButtonView: 버튼을 클릭하면 사용자가 역할을 얻는 뷰를 제공합니다.
"""

import discord
from discord.ext import commands

# 이모지와 대응하는 역할 ID를 정의합니다.
EMOJI_TO_ROLE: dict[str, int] = {"✅": 987654321098765432}
ROLE_MESSAGE_ID: int = 123456789012345678

# 버튼으로 부여할 역할 ID를 상수로 지정합니다.
DEV_ROLE_ID: int = 111111111111111111
DESIGNER_ROLE_ID: int = 222222222222222222


class ReactionRoleCog(commands.Cog):
    """리액션 추가/삭제 이벤트를 통해 역할을 관리하는 코그."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent) -> None:
        if payload.message_id != ROLE_MESSAGE_ID:
            return
        emoji = str(payload.emoji)
        role_id = EMOJI_TO_ROLE.get(emoji)
        if role_id is None:
            return
        guild = self.bot.get_guild(payload.guild_id)
        member = guild.get_member(payload.user_id)
        role = guild.get_role(role_id)
        if member and role:
            await member.add_roles(role, reason="리액션 역할 부여")

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload: discord.RawReactionActionEvent) -> None:
        if payload.message_id != ROLE_MESSAGE_ID:
            return
        emoji = str(payload.emoji)
        role_id = EMOJI_TO_ROLE.get(emoji)
        if role_id is None:
            return
        guild = self.bot.get_guild(payload.guild_id)
        member = guild.get_member(payload.user_id)
        role = guild.get_role(role_id)
        if member and role:
            await member.remove_roles(role, reason="리액션 역할 제거")


class RoleButtonView(discord.ui.View):
    """버튼 클릭을 통해 역할을 부여하는 뷰. persistent하게 사용하려면 timeout=None."""

    def __init__(self) -> None:
        super().__init__(timeout=None)

    @discord.ui.button(label="개발자", custom_id="role_dev", style=discord.ButtonStyle.primary)
    async def dev_button(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
        role = interaction.guild.get_role(DEV_ROLE_ID)
        if role:
            await interaction.user.add_roles(role)
            await interaction.response.send_message("개발자 역할이 부여되었습니다.", ephemeral=True)

    @discord.ui.button(label="디자이너", custom_id="role_designer", style=discord.ButtonStyle.primary)
    async def designer_button(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
        role = interaction.guild.get_role(DESIGNER_ROLE_ID)
        if role:
            await interaction.user.add_roles(role)
            await interaction.response.send_message("디자이너 역할이 부여되었습니다.", ephemeral=True)


# 실제 사용 시에는 다음과 같이 봇에 코그를 추가하고 메시지를 전송합니다.
if __name__ == "__main__":
    intents = discord.Intents.default()
    intents.members = True  # 리액션 역할을 위해 멤버 정보가 필요
    intents.message_content = True
    bot = commands.Bot(command_prefix="!", intents=intents)

    @bot.event
    async def on_ready() -> None:
        print(f"Logged in as {bot.user}")
        bot.add_cog(ReactionRoleCog(bot))
        # 채널에 리액션 역할 메시지 전송 (한 번만 실행해야 함)
        # channel = bot.get_channel(YOUR_CHANNEL_ID)
        # msg = await channel.send("✅ 이모지를 클릭하면 테스트 역할이 부여됩니다.")
        # global ROLE_MESSAGE_ID
        # ROLE_MESSAGE_ID = msg.id
        # await msg.add_reaction("✅")
        # 지속 버튼 뷰 등록
        # bot.add_view(RoleButtonView())

    # bot.run(os.getenv("DISCORD_TOKEN"))

