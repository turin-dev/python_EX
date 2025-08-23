"""
49장 – 하이브리드 명령 예제

이 모듈은 commands.hybrid_command()를 사용하여 하나의 함수로 메시지 명령과 슬래시 명령을
동시에 구현하는 방법을 보여준다.
"""

import discord
from discord.ext import commands


class PingCog(commands.Cog):
    """퐁 응답을 제공하는 코그."""

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.hybrid_command(name="핑", description="퐁!을 출력하는 명령", with_app_command=True)
    async def ping(self, ctx: commands.Context, times: int = 1) -> None:
        """times 회수만큼 '퐁!'을 반복해 응답한다."""
        # times는 1에서 5 사이로 제한한다.
        times = max(1, min(times, 5))
        for _ in range(times):
            await ctx.reply("퐁!", mention_author=False)


async def setup(bot: commands.Bot) -> None:
    """이 코그를 봇에 등록한다."""
    await bot.add_cog(PingCog(bot))

