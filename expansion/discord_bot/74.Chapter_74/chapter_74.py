"""
경제 시스템 예제.

이 모듈은 SQLite를 사용해 사용자별 포인트 잔액을 저장하고, 잔액 조회, 포인트
송금, 일일 보상 기능을 구현하는 예제입니다. 또한 서버 내 상점 시스템의
뼈대도 포함되어 있습니다.

필수 패키지: aiosqlite
설치: pip install aiosqlite
"""

from __future__ import annotations
import asyncio
import aiosqlite
import discord
from discord.ext import commands, tasks


class EconomyDB:
    """SQLite 기반 경제 데이터베이스."""
    def __init__(self, db_path: str = "economy.db") -> None:
        self.db_path = db_path
        self.lock = asyncio.Lock()

    async def init(self) -> None:
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                "CREATE TABLE IF NOT EXISTS balances (user_id INTEGER PRIMARY KEY, balance INTEGER NOT NULL DEFAULT 0)"
            )
            await db.execute(
                "CREATE TABLE IF NOT EXISTS shop (item TEXT PRIMARY KEY, price INTEGER NOT NULL)"
            )
            await db.commit()

    async def add_points(self, user_id: int, amount: int) -> None:
        async with self.lock:
            async with aiosqlite.connect(self.db_path) as db:
                await db.execute(
                    "INSERT INTO balances(user_id, balance) VALUES(?, ?) ON CONFLICT(user_id) DO UPDATE SET balance = balance + ?",
                    (user_id, amount, amount),
                )
                await db.commit()

    async def get_balance(self, user_id: int) -> int:
        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute("SELECT balance FROM balances WHERE user_id = ?", (user_id,)) as cursor:
                row = await cursor.fetchone()
                return row[0] if row else 0

    async def set_item(self, item: str, price: int) -> None:
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                "INSERT OR REPLACE INTO shop(item, price) VALUES(?, ?)", (item, price)
            )
            await db.commit()

    async def get_items(self) -> list[tuple[str, int]]:
        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute("SELECT item, price FROM shop") as cursor:
                return await cursor.fetchall()

    async def buy_item(self, user_id: int, item: str) -> bool:
        async with self.lock:
            async with aiosqlite.connect(self.db_path) as db:
                async with db.execute("SELECT price FROM shop WHERE item = ?", (item,)) as cursor:
                    row = await cursor.fetchone()
                    if not row:
                        return False
                    price = row[0]
                async with db.execute("SELECT balance FROM balances WHERE user_id = ?", (user_id,)) as cursor:
                    row = await cursor.fetchone()
                    balance = row[0] if row else 0
                if balance < price:
                    return False
                # 차감 및 저장
                await db.execute(
                    "UPDATE balances SET balance = balance - ? WHERE user_id = ?",
                    (price, user_id),
                )
                await db.commit()
                return True


class EconomyCog(commands.Cog):
    """포인트 잔액 조회, 송금 및 일일 보상을 제공하는 Cog."""
    def __init__(self, bot: commands.Bot, db: EconomyDB) -> None:
        self.bot = bot
        self.db = db
        self.daily_amount = 100
        # 일일 보상 받은 사용자 ID 집합
        self.claimed: set[int] = set()
        self.daily_reset_loop.start()

    @commands.command(name="balance")
    async def balance(self, ctx: commands.Context) -> None:
        bal = await self.db.get_balance(ctx.author.id)
        await ctx.send(f"{ctx.author.display_name}님의 잔액: {bal} 코인")

    @commands.command(name="give")
    async def give(self, ctx: commands.Context, member: discord.Member, amount: int) -> None:
        if amount <= 0:
            return await ctx.send("양수 금액을 입력하세요.")
        donor_bal = await self.db.get_balance(ctx.author.id)
        if donor_bal < amount:
            return await ctx.send("잔액이 부족합니다.")
        await self.db.add_points(ctx.author.id, -amount)
        await self.db.add_points(member.id, amount)
        await ctx.send(f"{ctx.author.display_name}님이 {member.display_name}님에게 {amount} 코인을 보냈습니다.")

    @commands.command(name="daily")
    async def daily(self, ctx: commands.Context) -> None:
        user_id = ctx.author.id
        if user_id in self.claimed:
            return await ctx.send("이미 오늘의 보상을 받으셨습니다. 내일 다시 시도하세요!")
        await self.db.add_points(user_id, self.daily_amount)
        self.claimed.add(user_id)
        await ctx.send(f"{self.daily_amount} 코인을 지급했습니다. 내일 또 찾아주세요!")

    @tasks.loop(hours=24)
    async def daily_reset_loop(self) -> None:
        self.claimed.clear()

    @daily_reset_loop.before_loop
    async def before_daily_reset(self) -> None:
        await self.bot.wait_until_ready()

    @commands.command(name="shop")
    async def shop(self, ctx: commands.Context) -> None:
        items = await self.db.get_items()
        if not items:
            return await ctx.send("상점에 아이템이 없습니다.")
        embed = discord.Embed(title="상점", description="아이템 목록과 가격")
        for item, price in items:
            embed.add_field(name=item, value=f"{price} 코인", inline=False)
        await ctx.send(embed=embed)

    @commands.command(name="buy")
    async def buy(self, ctx: commands.Context, *, item: str) -> None:
        success = await self.db.buy_item(ctx.author.id, item)
        if success:
            await ctx.send(f"{item} 아이템을 구매했습니다!")
            # 아이템에 따른 역할 부여 등 추가 처리 가능
        else:
            await ctx.send("구매 실패: 잔액이 부족하거나 아이템이 없습니다.")


async def setup(bot: commands.Bot) -> None:
    db = EconomyDB()
    await db.init()
    await bot.add_cog(EconomyCog(bot, db))