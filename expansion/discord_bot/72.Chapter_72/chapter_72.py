"""
동적 컴포넌트 및 모달 예제.

이 모듈은 외부 API 결과에 따라 셀렉트 메뉴 옵션을 동적으로 로딩하고,
모달을 여러 단계로 연결하는 예를 포함합니다.

1. GitHubRepoSelectView: 사용자의 깃허브 공개 저장소 목록을 API로 받아와
   셀렉트 메뉴 옵션으로 보여줍니다. 선택하면 결과를 에페멀(개인 메시지)로 회신합니다.
2. FeedbackModal: 두 단계 모달을 구현하여 사용자의 이름과 나이를 받고,
   두 번째 모달에서 의견을 작성하도록 합니다.

실제 사용 시에는 aiohttp 또는 requests를 설치해야 하며, GitHub API 토큰이
필요할 경우 헤더에 추가해야 합니다.
"""

from __future__ import annotations
import asyncio
from typing import List

import discord
from discord.ext import commands

try:
    import aiohttp
except ImportError:
    aiohttp = None


class GitHubRepoSelectView(discord.ui.View):
    """
    주어진 GitHub 사용자 이름의 공개 저장소를 로딩하여 셀렉트 메뉴로 표시하는 View.
    """
    def __init__(self, username: str):
        super().__init__(timeout=60)
        self.username = username
        # 비어 있는 Select를 먼저 만들고 이후에 옵션을 채움
        self.select = discord.ui.Select(placeholder="저장소 목록을 불러오는 중...", options=[])
        self.select.callback = self._on_select
        self.add_item(self.select)
        # 백그라운드에서 옵션을 로딩
        self.task = asyncio.create_task(self.load_options())

    async def load_options(self) -> None:
        if aiohttp is None:
            # aiohttp가 없으면 실패 메시지 표시
            self.select.placeholder = "aiohttp 미설치"
            await self.message.edit(view=self)
            return
        url = f"https://api.github.com/users/{self.username}/repos"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                data = await resp.json()
        # 첫 25개 저장소만 표시 (Discord 제한)
        options: List[discord.SelectOption] = []
        for repo in data[:25]:
            options.append(discord.SelectOption(label=repo.get("name"), value=repo.get("html_url")))
        self.select.placeholder = "저장소를 선택하세요"
        self.select.options = options
        await self.message.edit(view=self)

    async def _on_select(self, interaction: discord.Interaction) -> None:
        # 사용자가 선택한 저장소 URL 반환
        if not self.select.values:
            return
        url = self.select.values[0]
        await interaction.response.send_message(f"선택한 저장소 링크: {url}", ephemerial=True)
        self.stop()


class FeedbackStepOneModal(discord.ui.Modal, title="1단계: 기본 정보"):
    name = discord.ui.TextInput(label="이름", placeholder="닉네임", max_length=32)
    age = discord.ui.TextInput(label="나이", placeholder="숫자로 입력", max_length=3)

    async def on_submit(self, interaction: discord.Interaction) -> None:
        # 두 번째 모달로 연결
        await interaction.response.send_modal(FeedbackStepTwoModal(self.name.value, self.age.value))


class FeedbackStepTwoModal(discord.ui.Modal):
    def __init__(self, name: str, age: str) -> None:
        super().__init__(title="2단계: 의견 작성")
        self.name = name
        self.age = age
        self.comment = discord.ui.TextInput(
            label="의견", style=discord.TextStyle.long, placeholder="하고 싶은 말을 적어주세요", max_length=500
        )
        self.add_item(self.comment)

    async def on_submit(self, interaction: discord.Interaction) -> None:
        await interaction.response.send_message(
            f"감사합니다 {self.name}({self.age})님!\n의견: {self.comment.value}",
            ephemerial=True
        )


async def setup(bot: commands.Bot) -> None:
    @bot.command(name="github_repos")
    async def github_repos(ctx: commands.Context, username: str) -> None:
        """주어진 GitHub 사용자의 저장소 목록을 선택 메뉴로 보여줍니다."""
        view = GitHubRepoSelectView(username)
        view.message = await ctx.send(f"{username}의 저장소 불러오는 중...", view=view)

    @bot.tree.command(name="feedback")
    async def feedback(inter: discord.Interaction) -> None:
        """두 단계 모달을 통해 익명 의견을 받습니다."""
        await inter.response.send_modal(FeedbackStepOneModal())