# 33장 – SQLite 데이터베이스 통합

디스코드 봇에서 영구적인 데이터를 저장하려면 파일 기반 데이터베이스를 사용하는 것이 편리합니다. `sqlite3` 모듈은 별도의 서버 없이도 SQL 데이터베이스를 사용할 수 있도록 해 주며, Python 표준 라이브러리에 포함되어 있습니다. 이 장에서는 SQLite를 사용하여 테이블을 생성하고, 데이터를 삽입하고, 조회하는 방법을 알아봅니다【232817957113109†L82-L92】.

## 데이터베이스 연결과 테이블 생성

SQLite 데이터베이스는 하나의 파일로 저장됩니다. `sqlite3.connect()`를 호출하면 해당 파일이 생성되거나 열립니다. 접속 객체는 컨텍스트 매니저로 사용해 자동으로 연결을 닫을 수 있습니다.

```python
import sqlite3

def init_db():
    with sqlite3.connect("data.db") as conn:
        cur = conn.cursor()
        cur.execute("""
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            content TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)
        conn.commit()
```

`CREATE TABLE IF NOT EXISTS` 구문은 테이블이 없을 때만 생성합니다. 기본 키를 자동 증가하도록 설정할 수 있습니다.

## 데이터 삽입과 조회

봇 명령어에서 메모를 저장하고 검색하는 예를 들어보겠습니다. 데이터 입력 시 SQL 인젝션을 방지하려면 파라미터 바인딩(`?`)을 사용해야 합니다.

```python
@bot.command()
async def 메모(ctx, *, content: str):
    user_id = ctx.author.id
    with sqlite3.connect("data.db") as conn:
        cur = conn.cursor()
        cur.execute("INSERT INTO notes (user_id, content) VALUES (?, ?)", (user_id, content))
        conn.commit()
    await ctx.send("메모가 저장되었습니다.")

@bot.command()
async def 메모확인(ctx):
    user_id = ctx.author.id
    with sqlite3.connect("data.db") as conn:
        cur = conn.cursor()
        cur.execute("SELECT content, created_at FROM notes WHERE user_id = ? ORDER BY id DESC LIMIT 5", (user_id,))
        rows = cur.fetchall()
    if not rows:
        await ctx.send("저장된 메모가 없습니다.")
    else:
        messages = [f"• {content} (작성일: {created_at})" for content, created_at in rows]
        await ctx.send("\n".join(messages))
```

이 예제에서는 사용자의 최근 5개 메모를 조회하여 메시지로 출력합니다. 트랜잭션은 커서 실행 후 `commit()`을 호출하여 반영하며, 읽기 전용 작업에는 필요 없습니다.

## 주의사항

SQLite는 단일 파일 기반이므로 여러 스레드 또는 프로세스가 동시에 쓰기를 시도하면 `OperationalError: database is locked` 오류가 발생할 수 있습니다. 이를 해결하려면 단일 쓰기 작업만 수행하거나, 외부 데이터베이스 서버(MySQL, PostgreSQL 등)로 이전하는 것이 좋습니다. 또한 대량의 데이터를 처리해야 한다면 ORM 라이브러리(`SQLAlchemy`)의 비동기 지원을 고려할 수 있습니다.

## 요약

`sqlite3` 모듈을 사용하면 복잡한 설정 없이도 SQL 데이터베이스를 활용할 수 있습니다. 테이블을 적절히 설계하고, 바인딩 파라미터를 사용하여 보안을 유지하며, 데이터 경합이 많은 경우에는 별도의 데이터베이스 서버를 사용하세요.

