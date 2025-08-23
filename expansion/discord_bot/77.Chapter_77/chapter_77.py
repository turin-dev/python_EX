"""
임베드와 리치 메시지 예제.

이 스크립트는 다중 페이지 도움말 시스템을 구현합니다. 각 페이지는 embed로
구성되며, 두 개의 버튼으로 앞뒤 페이지를 이동할 수 있습니다. timeout 후
버튼은 비활성화됩니다.
"""

from __future__ import annotations
import discord
from discord.ext import commands


class PagedHelpView(discord.ui.View):
    def __init__(self, pages: list[discord.Embed], timeout: float = 120.0) -> None:
        super().__init__(timeout=timeout)
        self.pages = pages
        self.index = 0

    async def update(self, interaction: discord.Interaction) -> None:
        await interaction.response.edit_message(embed=self.pages[self.index], view=self)

    @discord.ui.button(label="◀", style=discord.ButtonStyle.secondary)
    async def previous_page(self, button: discord.ui.Button, interaction: discord.Interaction) -> None:
        self.index = (self.index - 1) % len(self.pages)
        await self.update(interaction)

    @discord.ui.button(label="▶", style=discord.ButtonStyle.secondary)
    async def next_page(self, button: discord.ui.Button, interaction: discord.Interaction) -> None:
        self.index = (self.index + 1) % len(self.pages)
        await self.update(interaction)


async def setup(bot: commands.Bot) -> None:
    @bot.command(name="richhelp")
    async def rich_help(ctx: commands.Context) -> None:
        """Embed 페이지를 사용하는 도움말 명령."""
        pages = []
        pages.append(
            discord.Embed(
                title="도움말 1", description="봇 사용 방법의 기본을 설명하는 첫 번째 페이지", color=discord.Color.blue()
            )
        )
        pages.append(
            discord.Embed(
                title="도움말 2", description="두 번째 페이지 내용", color=discord.Color.green()
            )
        )
        pages.append(
            discord.Embed(
                title="도움말 3", description="세 번째 페이지 내용", color=discord.Color.purple()
            )
        )
        view = PagedHelpView(pages)
        await ctx.send(embed=pages[0], view=view)