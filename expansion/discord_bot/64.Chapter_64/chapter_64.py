"""환경 변수와 비밀 관리 예제.

이 모듈은 `.env` 파일을 로드하여 디스코드 토큰과 데이터베이스 URL을
읽어오는 예제를 보여줍니다. `python-dotenv` 패키지가 필요합니다.
"""

import os
from dotenv import load_dotenv

load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
DATABASE_URL = os.getenv("DATABASE_URL")

if __name__ == "__main__":
    print("DISCORD_TOKEN:", DISCORD_TOKEN)
    print("DATABASE_URL:", DATABASE_URL)

