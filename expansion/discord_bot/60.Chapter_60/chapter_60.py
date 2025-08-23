"""모니터링과 메트릭 예제.

이 모듈은 로깅 설정과 명령 호출 횟수를 수집하는 StatsCog를 제공합니다.
실제 봇에서 import하여 사용하세요.
"""

import logging
import logging.config
from collections import Counter

import discord
from discord.ext import commands


# 로깅 설정 예제
LOGGING_CONFIG = {
    "version": 1,
    "formatters": {
        "standard": {
            "format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "standard",
            "level": "INFO",
        },
        "file": {
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "standard",
            "filename": "bot.log",
            "maxBytes": 1024 * 1024,
            "backupCount": 3,
            "level": "DEBUG",
        },
    },
    "root": {
        "handlers": ["console", "file"],
        "level": "DEBUG",
    },
}


class StatsCog(commands.Cog):
    """명령 사용 통계를 기록하고 출력하는 코그."""

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.command_calls: Counter[str] = Counter()

    @commands.Cog.listener()
    async def on_command(self, ctx: commands.Context) -> None:
        # 모든 명령 호출 시 카운터 증가
        self.command_calls[ctx.command.qualified_name] += 1

    @commands.hybrid_command(name="stats", description="명령 사용 통계를 출력합니다")
    async def stats(self, ctx: commands.Context) -> None:
        if not self.command_calls:
            await ctx.send("현재까지 수집된 통계가 없습니다.")
            return
        lines = [f"{name}: {count}" for name, count in self.command_calls.items()]
        report = "\n".join(lines)
        await ctx.send(f"명령 사용 통계:\n{report}")


def setup_logging() -> logging.Logger:
    """로깅 구성을 적용하고 루트 로거를 반환합니다."""
    logging.config.dictConfig(LOGGING_CONFIG)
    logger = logging.getLogger(__name__)
    logger.info("로깅이 초기화되었습니다")
    return logger


if __name__ == "__main__":
    # 로깅 초기화
    logger = setup_logging()
    intents = discord.Intents.default()
    intents.message_content = True
    bot = commands.Bot(command_prefix="!", intents=intents)
    # StatsCog 등록
    bot.add_cog(StatsCog(bot))

    @bot.event
    async def on_ready() -> None:
        logger.info("Bot ready")

    # bot.run(os.getenv("DISCORD_TOKEN"))

