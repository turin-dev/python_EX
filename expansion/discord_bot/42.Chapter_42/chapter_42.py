"""
42장 – 지속적인 뷰 예제

이 모듈은 봇 재시작에도 동작하는 지속적인 역할 관리 뷰를 구현한다. 뷰의 `timeout`이
`None`으로 설정되고 모든 버튼에 `custom_id`가 지정되어 있으면 persistent view가 된다.
봇이 시작될 때 `bot.add_view(RoleView(role))`를 호출하여 뷰를 등록해야 한다.
"""

import discord
from discord.ext import commands


class RoleView(discord.ui.View):
    """지속적인 역할 관리 뷰."""

    def __init__(self, role: discord.Role) -> None:
        super().__init__(timeout=None)  # persistent view
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

    async def join_callback(self, interaction: discord.Interaction) -> None:
        """사용자에게 역할을 부여하는 콜백."""
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

    async def leave_callback(self, interaction: discord.Interaction) -> None:
        """사용자에게서 역할을 제거하는 콜백."""
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


async def setup(bot: commands.Bot) -> None:
    """봇 시작 시 RoleView를 등록합니다.

    이 함수는 `discord.ext.commands.Bot.setup_hook`에서 호출됩니다.
    각 길드마다 적절한 역할 ID를 지정하여 RoleView를 추가하세요.
    """
    async def on_ready_once() -> None:
        if not bot.guilds:
            return
        guild = bot.guilds[0]
        # 실제 역할 ID로 교체하세요.
        role_id = 123456789012345678
        role = guild.get_role(role_id)
        if role:
            bot.add_view(RoleView(role))

    bot.add_listener(on_ready_once, name="on_ready")

