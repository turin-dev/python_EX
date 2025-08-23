"""
48장 – 배포와 환경 관리 예제

이 모듈은 INI 구성 파일과 환경 변수를 사용하는 설정 로딩 예제를 제공한다.
"""

import os
import configparser


def load_config(path: str = "config.ini") -> dict:
    """INI 파일과 환경 변수를 읽어 설정 딕셔너리를 반환한다."""
    config = configparser.ConfigParser()
    config.read(path, encoding="utf-8")
    # 환경 변수 우선순위로 토큰을 읽음
    token = os.environ.get("DISCORD_TOKEN", config.get("bot", "token", fallback=None))
    prefix = config.get("bot", "prefix", fallback="!")
    db_url = config.get("database", "url", fallback=None)
    return {"token": token, "prefix": prefix, "db_url": db_url}


if __name__ == "__main__":
    settings = load_config()
    print(settings)

