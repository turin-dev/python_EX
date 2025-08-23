"""
44장 – 슬래시 명령 그룹 예제

이 모듈은 슬래시 명령 그룹을 생성하는 방법을 보여준다. 그룹을 사용하면
관련 명령을 계층 구조로 묶어 관리할 수 있으며, 기본 권한과 설명을 지정할 수 있다.
"""

import discord
from discord.ext import commands


class ReportGroup(discord.app_commands.Group):
    """버그와 기능 요청을 처리하는 슬래시 명령 그룹."""

    def __init__(self) -> None:
        super().__init__(
            name="신고",
            description="버그 또는 기능 요청을 접수합니다",
            guild_only=True
        )

    @discord.app_commands.command(name="버그", description="버그를 신고합니다")
    async def bug(self, interaction: discord.Interaction, title: str, description: str) -> None:
        """버그 리포트 서브커맨드."""
        # 실제 구현에서는 DB나 이슈 트래킹 시스템에 저장합니다.
        await interaction.response.send_message(
            f"버그 '{title}'가 접수되었습니다!",
            allowed_mentions=discord.AllowedMentions.none(),
            ephemeral=True
        )

    @discord.app_commands.command(name="기능", description="새로운 기능을 제안합니다")
    async def feature(self, interaction: discord.Interaction, title: str, description: str) -> None:
        """기능 요청 서브커맨드."""
        await interaction.response.send_message(
            f"기능 요청 '{title}'가 접수되었습니다!",
            allowed_mentions=discord.AllowedMentions.none(),
            ephemeral=True
        )


async def setup(bot: commands.Bot) -> None:
    """봇에 명령 그룹을 등록합니다."""
    group = ReportGroup()
    bot.tree.add_command(group)

    @bot.event
    async def on_ready() -> None:
        # 전역 명령 동기화
        await bot.tree.sync()
        print("신고 명령 그룹이 동기화되었습니다.")

