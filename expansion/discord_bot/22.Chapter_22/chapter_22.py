"""로깅 설정 예제.

이 스크립트는 discord.py 봇을 위한 기본 로깅 구성을 보여 줍니다.
콘솔과 파일에 로그를 남기고, 커스텀 로거를 사용하는 방법을 포함합니다.
"""

import logging
import discord
from discord.ext import commands


# 기본 로깅 설정: 콘솔과 파일 모두에 INFO 이상의 로그를 기록합니다.
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("bot.log", encoding="utf-8")
    ]
)

# discord.py 내부 로거 설정
discord.utils.setup_logging()


# 커스텀 로거 생성 예: 데이터베이스와 관련된 로그만 별도 파일에 저장
db_logger = logging.getLogger("bot.database")
db_logger.setLevel(logging.INFO)
db_logger.addHandler(logging.FileHandler("db.log", encoding="utf-8"))


bot = commands.Bot(command_prefix="!", intents=discord.Intents.default())


@bot.event
async def on_ready():
    # 봇이 로그인하면 로그 출력
    logging.getLogger(__name__).info("봇이 준비되었습니다.")
    db_logger.info("데이터베이스가 준비되었습니다.")


if __name__ == "__main__":
    # bot.run("YOUR_TOKEN")
    pass