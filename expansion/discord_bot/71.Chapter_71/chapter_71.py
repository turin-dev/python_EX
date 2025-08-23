"""
설문과 투표 시스템 예제.

이 스크립트는 두 가지 방식의 투표를 제공합니다.

1. ReactionPollCog: 👍/👎 리액션으로 찬반 투표를 진행합니다. 중복 투표를 방지하고
   결과를 집계합니다.
2. ButtonPollView: 버튼을 통해 여러 옵션을 제시하고, 사용자 투표를 수집한 뒤
   결과를 표시합니다. View는 timeout 후 자동으로 종료됩니다.

봇에 이 Cog와 View를 등록하고 명령어를 사용해 설문을 시작할 수 있습니다.
"""

from __future__ import annotations
import asyncio
from typing import Dict, Set

import discord
from discord.ext import commands


class ReactionPollCog(commands.Cog):
    """👍/👎 리액션을 사용한 찬반 투표 Cog."""
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        # message_id -> {user_id: emoji}
        self.votes: Dict[int, Dict[int, str]] = {}

    @commands.command(name="vote")
    async def create_vote(self, ctx: commands.Context, *, question: str) -> None:
        """투표 메시지를 보내고 반응을 붙입니다."""
        msg = await ctx.send(f"{question}\n👍 = 찬성, 👎 = 반대")
        # 반응 추가
        await msg.add_reaction("👍")
        await msg.add_reaction("👎")
        self.votes[msg.id] = {}

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent) -> None:
        # 봇이 추가한 반응은 무시
        if payload.user_id == self.bot.user.id:
            return
        if payload.message_id not in self.votes:
            return
        emoji_str = str(payload.emoji)
        # 허용된 이모지만 처리
        if emoji_str not in ("👍", "👎"):
            return
        user_votes = self.votes[payload.message_id]
        # 다른 표를 이미 찍었다면 제거
        for uid, prev in list(user_votes.items()):
            if uid == payload.user_id and prev != emoji_str:
                channel = self.bot.get_channel(payload.channel_id)
                if channel:
                    message = await channel.fetch_message(payload.message_id)
                    # member는 None일 수 있으므로 fetch하여 삭제
                    user = payload.member or (await self.bot.fetch_user(payload.user_id))
                    await message.remove_reaction(prev, user)
        user_votes[payload.user_id] = emoji_str


class ButtonPollView(discord.ui.View):
    """버튼 기반 설문 View."""
    def __init__(self, options: list[str], timeout: float = 60.0) -> None:
        super().__init__(timeout=timeout)
        self.options = options
        self.results: Dict[str, Set[int]] = {opt: set() for opt in options}
        # 옵션 버튼 생성
        for idx, opt in enumerate(options):
            # 각 버튼에 고유 custom_id를 부여해야 persistent View를 만들 수 있음
            custom_id = f"poll_option_{idx}"
            button = discord.ui.Button(label=opt, style=discord.ButtonStyle.primary, custom_id=custom_id)
            button.callback = self.make_vote_callback(opt)
            self.add_item(button)
        # 종료 버튼
        end_button = discord.ui.Button(label="종료", style=discord.ButtonStyle.danger, row=1)
        end_button.callback = self.end_poll
        self.add_item(end_button)

    def make_vote_callback(self, option: str):
        async def callback(interaction: discord.Interaction) -> None:
            user_id = interaction.user.id
            # 중복 투표 제거: 다른 옵션에서 사용자 ID 제거
            for opt, voters in self.results.items():
                voters.discard(user_id)
            self.results[option].add(user_id)
            await interaction.response.defer()  # 응답 지연 (버튼 상태 유지)
        return callback

    async def end_poll(self, interaction: discord.Interaction) -> None:
        """투표를 종료하고 결과를 출력합니다."""
        # 모든 버튼 비활성화
        for child in self.children:
            if isinstance(child, discord.ui.Button):
                child.disabled = True
        summary = "\n".join(f"{opt}: {len(voters)}표" for opt, voters in self.results.items())
        await interaction.response.edit_message(view=self)
        await interaction.followup.send(f"투표 종료! 결과:\n{summary}")
        self.stop()

    async def on_timeout(self) -> None:
        # 시간이 초과되면 종료 버튼 호출
        summary = "\n".join(f"{opt}: {len(voters)}표" for opt, voters in self.results.items())
        channel = self.message.channel if self.message else None
        if channel:
            await channel.send(f"투표 시간 초과! 결과:\n{summary}")


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(ReactionPollCog(bot))

    @bot.command(name="button_poll")
    async def start_button_poll(ctx: commands.Context, *options: str) -> None:
        """버튼 기반 투표를 시작합니다. 옵션은 2개 이상 입력하세요."""
        if len(options) < 2:
            return await ctx.send("최소 두 개의 옵션을 입력하세요.")
        view = ButtonPollView(list(options))
        await ctx.send("버튼 투표에 참여하세요!", view=view)