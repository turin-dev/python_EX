"""커맨드 카테고리와 도움말 커스터마이징 예제.

이 모듈은 Cog를 사용해 명령을 분류하고, MinimalHelpCommand를
상속해 도움말 메시지를 임베드 형식으로 출력하는 예제를 제공합니다.
"""

import discord
from discord.ext import commands


class UtilityCog(commands.Cog, name="유틸리티", description="유용한 일반 명령 모음"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="핑")
    async def ping(self, ctx: commands.Context) -> None:
        """봇의 지연 시간을 확인합니다."""
        latency_ms = round(self.bot.latency * 1000)
        await ctx.send(f"Pong! {latency_ms}ms")


class MyHelpCommand(commands.MinimalHelpCommand):
    """명령어 목록을 임베드로 표시하는 커스텀 도움말."""

    def get_command_signature(self, command: commands.Command) -> str:
        return f"{self.clean_prefix}{command.qualified_name} {command.signature}".strip()

    async def send_bot_help(self, mapping: dict) -> None:
        embed = discord.Embed(title="도움말", color=0x00BFFF)
        for cog, commands_ in mapping.items():
            filtered = await self.filter_commands(commands_, sort=True)
            if not filtered:
                continue
            name = cog.qualified_name if cog else "기타"
            value = "\n".join(f"• {self.get_command_signature(c)}" for c in filtered)
            embed.add_field(name=name, value=value, inline=False)
        channel = self.get_destination()
        await channel.send(embed=embed)


def create_bot() -> commands.Bot:
    intents = discord.Intents.default()
    intents.message_content = True
    bot = commands.Bot(command_prefix="!", intents=intents, help_command=MyHelpCommand())
    bot.add_cog(UtilityCog(bot))
    return bot


if __name__ == "__main__":
    bot = create_bot()
    @bot.event
    async def on_ready() -> None:
        print("Bot ready with custom help")
    # bot.run(os.getenv("DISCORD_TOKEN"))

