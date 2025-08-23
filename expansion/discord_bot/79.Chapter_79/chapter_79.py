"""
맞춤형 도움말 시스템 예제.

이 스크립트는 두 가지 도움말 방식을 제공합니다:

1. EmbedHelpCommand: MinimalHelpCommand를 상속하여 Cog별 명령 목록을
   임베드로 출력합니다.
2. HelpMenuView: Cog 이름을 버튼으로 보여주고, 버튼을 클릭하면 해당 Cog의
   명령을 임베드로 보여주는 인터랙티브 도움말.

봇 생성 시 `help_command` 파라미터에 EmbedHelpCommand를 전달하거나,
메뉴 방식 도움말 명령을 등록해 사용할 수 있습니다.
"""

from __future__ import annotations
import discord
from discord.ext import commands


class EmbedHelpCommand(commands.MinimalHelpCommand):
    """임베드 기반 최소 도움말 명령."""
    async def send_bot_help(self, mapping):
        embed = discord.Embed(title="도움말", description="사용 가능한 명령 목록")
        for cog, cmds in mapping.items():
            filtered = await self.filter_commands(cmds, sort=True)
            if not filtered:
                continue
            cog_name = getattr(cog, "qualified_name", "기타")
            cmd_list = ", ".join(cmd.name for cmd in filtered)
            embed.add_field(name=cog_name, value=cmd_list, inline=False)
        channel = self.get_destination()
        await channel.send(embed=embed)


class HelpMenuView(discord.ui.View):
    """버튼 기반 도움말 메뉴."""
    def __init__(self, bot: commands.Bot):
        super().__init__(timeout=120)
        self.bot = bot
        for cog_name, cog in bot.cogs.items():
            button = discord.ui.Button(label=cog_name, style=discord.ButtonStyle.primary)
            button.callback = self.make_cog_callback(cog)
            self.add_item(button)

    def make_cog_callback(self, cog):
        async def callback(interaction: discord.Interaction):
            cmds = cog.get_commands()
            embed = discord.Embed(title=f"{cog.qualified_name} 명령", description="")
            for cmd in cmds:
                embed.add_field(name=cmd.name, value=cmd.help or "설명 없음", inline=False)
            await interaction.response.send_message(embed=embed, ephemerial=True)
        return callback


async def setup(bot: commands.Bot) -> None:
    # EmbedHelpCommand를 사용하려면 봇 생성 시 help_command에 전달
    bot.help_command = EmbedHelpCommand()

    @bot.command(name="help_menu")
    async def help_menu(ctx: commands.Context) -> None:
        view = HelpMenuView(ctx.bot)
        await ctx.send("도움말 카테고리를 선택하세요", view=view)