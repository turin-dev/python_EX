"""
45장 – 고급 모달 예제

이 모듈은 여러 입력 필드를 가진 모달을 구현하고, 제출 시 데이터를 검증하는 방법을 보여준다.
"""

import discord
from discord import ui
from discord.ext import commands


class FeedbackModal(ui.Modal, title="피드백 제출"):
    """사용자 피드백을 입력받는 모달."""

    name: ui.TextInput = ui.TextInput(
        label="이름",
        placeholder="닉네임 또는 실명",
        max_length=32
    )
    rating: ui.TextInput = ui.TextInput(
        label="평점 (1~5)",
        placeholder="숫자로 입력",
        max_length=1
    )
    comment: ui.TextInput = ui.TextInput(
        label="의견",
        style=discord.TextStyle.paragraph,
        required=False,
        max_length=500
    )

    async def on_submit(self, interaction: discord.Interaction) -> None:
        """제출 시 입력값을 검증하고 응답한다."""
        # 평점 범위 검증
        try:
            score = int(self.rating.value)
            if not 1 <= score <= 5:
                raise ValueError
        except ValueError:
            await interaction.response.send_message(
                "평점은 1에서 5 사이의 숫자여야 합니다.",
                allowed_mentions=discord.AllowedMentions.none(),
                ephemeral=True
            )
            return

        # 피드백 처리 로직 (DB에 저장하거나 로그 등)
        await interaction.response.send_message(
            f"{self.name.value}님의 피드백이 접수되었습니다. 감사합니다!",
            allowed_mentions=discord.AllowedMentions.none(),
            ephemeral=True
        )

    async def on_error(self, interaction: discord.Interaction, error: Exception) -> None:
        """모달 처리 중 오류가 발생했을 때 호출된다."""
        await interaction.response.send_message(
            "모달 처리 중 오류가 발생했습니다.",
            allowed_mentions=discord.AllowedMentions.none(),
            ephemeral=True
        )


async def setup(bot: commands.Bot) -> None:
    """봇에 피드백 명령을 등록한다."""
    @bot.tree.command(name="피드백", description="피드백 폼을 표시합니다")
    async def feedback_cmd(interaction: discord.Interaction) -> None:
        await interaction.response.send_modal(FeedbackModal())

