"""
46장 – 로깅과 메트릭 예제

이 모듈은 봇에서 Python logging을 설정하고 명령 사용량을 측정하는 간단한 예제를 제공한다.
"""

import logging
from collections import Counter

from discord.ext import commands


def setup_logging() -> None:
    """루트 로거와 discord 로거를 설정한다."""
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    formatter = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    # 콘솔 핸들러
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)
    # 파일 핸들러
    file_handler = logging.FileHandler("bot.log", encoding="utf-8")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    # discord.py 내부 로거 설정
    discord_logger = logging.getLogger("discord")
    discord_logger.setLevel(logging.WARNING)


class MetricsCog(commands.Cog):
    """명령 실행 횟수를 수집하는 코그."""

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.command_counts: Counter[str] = Counter()

    @commands.Cog.listener()
    async def on_command_completion(self, ctx: commands.Context) -> None:
        name = ctx.command.qualified_name
        self.command_counts[name] += 1
        total = self.command_counts[name]
        # 10번마다 로그 출력
        if total % 10 == 0:
            logging.getLogger(__name__).info(
                "명령 '%s'가 총 %s회 호출되었습니다.", name, total
            )


async def setup(bot: commands.Bot) -> None:
    """로깅과 메트릭 코그를 설정한다."""
    setup_logging()
    await bot.add_cog(MetricsCog(bot))

