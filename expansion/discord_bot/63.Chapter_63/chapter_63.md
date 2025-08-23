# 비동기 데이터베이스 통합

봇이 사용자 데이터나 설정을 영구적으로 저장해야 한다면 데이터베이스를 사용해야 합니다. `discord.py`는 내부에 저장 기능을 제공하지 않으므로, 별도의 데이터베이스와 비동기 클라이언트를 사용해야 합니다. 이 장에서는 **SQLite**를 위한 `aiosqlite`와 **PostgreSQL**을 위한 `asyncpg` 예제를 소개합니다.

## aiosqlite로 간단한 DB 사용

SQLite는 파일 기반의 가벼운 데이터베이스로, 설정이 필요 없고 디스크에 단일 파일로 저장됩니다. `aiosqlite`는 비동기 SQLite 클라이언트로, 여러 코루틴에서 동시에 접근할 수 있도록 설계되어 있습니다. 다음은 사용자 포인트를 저장하는 테이블을 생성하고 값을 읽고 쓰는 함수입니다:

```python
import aiosqlite

DB_PATH = "data.db"

async def init_db():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            """CREATE TABLE IF NOT EXISTS user_points (
                    user_id INTEGER PRIMARY KEY,
                    points  INTEGER NOT NULL DEFAULT 0
            )"""
        )
        await db.commit()

async def add_points(user_id: int, amount: int):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "INSERT INTO user_points (user_id, points) VALUES (?, ?)"
            "ON CONFLICT(user_id) DO UPDATE SET points = points + ?",
            (user_id, amount, amount),
        )
        await db.commit()

async def get_points(user_id: int) -> int:
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute(
            "SELECT points FROM user_points WHERE user_id = ?",
            (user_id,)
        ) as cursor:
            row = await cursor.fetchone()
            return row[0] if row else 0
```

위 함수를 코그에서 호출하여 사용자에게 포인트를 지급하거나 조회할 수 있습니다. SQLite는 경량이지만 파일 잠금의 제약이 있으므로, 사용량이 많거나 여러 인스턴스에서 접근하는 경우에는 다른 DB를 선택하는 것이 좋습니다.

## asyncpg로 PostgreSQL 사용

PostgreSQL은 더 강력한 기능과 동시성을 제공하며, `asyncpg` 클라이언트를 통해 비동기로 사용할 수 있습니다. 사용 방법은 `aiosqlite`와 유사하지만, 데이터베이스 풀을 생성해 연결을 재사용하는 것이 일반적입니다:

```python
import asyncpg

async def create_pool():
    return await asyncpg.create_pool(dsn="postgresql://user:password@host/dbname")

async def add_points(pool: asyncpg.Pool, user_id: int, amount: int):
    async with pool.acquire() as conn:
        await conn.execute(
            "INSERT INTO user_points (user_id, points) VALUES ($1, $2)"
            "ON CONFLICT (user_id) DO UPDATE SET points = user_points.points + $2",
            user_id, amount
        )

async def get_points(pool: asyncpg.Pool, user_id: int) -> int:
    async with pool.acquire() as conn:
        row = await conn.fetchrow("SELECT points FROM user_points WHERE user_id = $1", user_id)
        return row["points"] if row else 0
```

PostgreSQL을 사용하면 여러 샤드나 인스턴스에서 동일한 데이터를 공유할 수 있으며, 복잡한 쿼리와 트랜잭션을 지원합니다. 그러나 초기 설정이 필요하고, 연결 풀을 적절히 관리해야 합니다.

## 요약

데이터베이스를 통해 봇의 상태와 사용자 데이터를 안전하게 저장할 수 있습니다. SQLite는 간단한 프로젝트에 적합하며, 더 큰 규모나 분산 환경에서는 PostgreSQL과 같은 외부 DB를 사용하는 것이 바람직합니다. 비동기 클라이언트를 사용하면 봇의 이벤트 루프를 막지 않고도 데이터베이스 작업을 수행할 수 있습니다.

