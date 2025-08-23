"""SQLite 통합 예제.

사용자 메모를 저장하고 최근 메모를 조회하는 명령어를 구현합니다.
"""

import sqlite3
import discord
from discord.ext import commands

DB_PATH = "data.db"


def init_db() -> None:
    """데이터베이스와 테이블을 초기화합니다."""
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor()
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS notes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                content TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        conn.commit()


bot = commands.Bot(command_prefix="!", intents=discord.Intents.default())


@bot.event
async def on_ready() -> None:
    init_db()
    print("데이터베이스가 초기화되었습니다.")


@bot.command(name="메모")
async def add_note(ctx: commands.Context, *, content: str) -> None:
    user_id = ctx.author.id
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO notes (user_id, content) VALUES (?, ?)",
            (user_id, content),
        )
        conn.commit()
    await ctx.send("메모가 저장되었습니다.")


@bot.command(name="메모확인")
async def show_notes(ctx: commands.Context) -> None:
    user_id = ctx.author.id
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor()
        cur.execute(
            "SELECT content, created_at FROM notes WHERE user_id = ? ORDER BY id DESC LIMIT 5",
            (user_id,),
        )
        rows = cur.fetchall()
    if not rows:
        await ctx.send("저장된 메모가 없습니다.")
        return
    lines = [f"• {content} (작성일: {created_at})" for content, created_at in rows]
    await ctx.send("\n".join(lines))


if __name__ == "__main__":
    # bot.run("YOUR_TOKEN")
    pass