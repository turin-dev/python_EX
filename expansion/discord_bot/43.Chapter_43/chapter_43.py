"""
43장 – 고급 셀렉트 메뉴 예제

이 모듈은 여러 값을 선택할 수 있는 셀렉트 메뉴와 채널 선택 메뉴를 구현한다. 사용자 정의
옵션 리스트를 사용하거나 특수 셀렉트 클래스로 채널을 선택하는 예제를 포함한다.
"""

import discord
from discord.ext import commands


class FruitView(discord.ui.View):
    """과일 선택을 위한 셀렉트 메뉴."""

    def __init__(self) -> None:
        super().__init__()
        options = [
            discord.SelectOption(label="사과", value="apple", description="상큼한 사과"),
            discord.SelectOption(label="바나나", value="banana", description="달콤한 바나나"),
            discord.SelectOption(label="체리", value="cherry", description="새콤한 체리"),
            discord.SelectOption(label="수박", value="watermelon", description="시원한 수박"),
            discord.SelectOption(label="포도", value="grape", description="맛있는 포도")
        ]
        select = discord.ui.Select(
            placeholder="좋아하는 과일을 선택하세요",
            min_values=1,
            max_values=3,
            options=options,
            custom_id="fruit_select"
        )
        select.callback = self.on_select
        self.add_item(select)

    async def on_select(self, interaction: discord.Interaction) -> None:
        values = interaction.data.get("values", [])
        chosen = ", ".join(values) if values else "없음"
        await interaction.response.send_message(
            f"선택한 과일: {chosen}",
            allowed_mentions=discord.AllowedMentions.none(),
            ephemeral=True
        )


class AnnouncementView(discord.ui.View):
    """공지 채널 선택 메뉴."""

    def __init__(self) -> None:
        super().__init__()
        select = discord.ui.ChannelSelect(
            channel_types=[discord.ChannelType.text],
            placeholder="공지 채널을 선택하세요",
            min_values=1,
            max_values=1,
            custom_id="channel_select"
        )
        select.callback = self.on_select
        self.add_item(select)

    async def on_select(self, interaction: discord.Interaction) -> None:
        # interaction.data['values']는 선택된 채널 ID 문자열 목록입니다.
        channel_id_str = interaction.data["values"][0]
        channel = interaction.guild.get_channel(int(channel_id_str))
        if channel:
            await interaction.response.send_message(
                f"선택한 채널: {channel.mention}",
                allowed_mentions=discord.AllowedMentions.none(),
                ephemeral=True
            )
        else:
            await interaction.response.send_message(
                "채널을 찾을 수 없습니다.",
                allowed_mentions=discord.AllowedMentions.none(),
                ephemeral=True
            )


async def setup(bot: commands.Bot) -> None:
    """봇 명령어를 등록하는 setup 함수."""

    @bot.command(name="과일")
    async def fruit_cmd(ctx: commands.Context) -> None:
        """과일 선택 메시지를 보냅니다."""
        await ctx.send("과일을 선택하세요", view=FruitView())

    @bot.command(name="공지채널")
    async def announce_cmd(ctx: commands.Context) -> None:
        """공지 채널 선택 메시지를 보냅니다."""
        await ctx.send("공지 채널을 선택하세요", view=AnnouncementView())

