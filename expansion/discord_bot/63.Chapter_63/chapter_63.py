"""비동기 데이터베이스 통합 예제.

이 모듈은 `aiosqlite`를 이용하여 사용자 포인트를 저장하고 조회하는
함수를 제공합니다. 실제 프로젝트에서는 데이터베이스 경로와 테이블
구조를 환경에 맞게 조정하세요.
"""

import aiosqlite

DB_PATH = "data.db"


async def init_db() -> None:
    """user_points 테이블을 생성합니다."""
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            """
            CREATE TABLE IF NOT EXISTS user_points (
                user_id INTEGER PRIMARY KEY,
                points  INTEGER NOT NULL DEFAULT 0
            )
            """
        )
        await db.commit()


async def add_points(user_id: int, amount: int) -> None:
    """주어진 사용자에게 포인트를 추가합니다."""
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            """
            INSERT INTO user_points (user_id, points) VALUES (?, ?)
            ON CONFLICT(user_id) DO UPDATE SET points = points + ?
            """,
            (user_id, amount, amount),
        )
        await db.commit()


async def get_points(user_id: int) -> int:
    """주어진 사용자의 포인트를 반환합니다."""
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute(
            "SELECT points FROM user_points WHERE user_id = ?",
            (user_id,),
        ) as cursor:
            row = await cursor.fetchone()
            return row[0] if row else 0

