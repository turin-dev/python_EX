# 경제 시스템과 포인트 관리

커뮤니티 활동을 장려하기 위해 봇에 **포인트 시스템**을 도입할 수 있습니다. 사용자가
메시지를 보내거나 특정 명령을 수행할 때 포인트를 지급하고, 포인트로 역할을
구매하거나 순위표를 만드는 등의 기능을 제공할 수 있습니다. 이 장에서는 간단한
경제 시스템을 설계하고 데이터베이스를 통해 포인트를 안전하게 저장하는 방법,
일일 보상을 자동으로 지급하는 스케줄링 기법 등을 설명합니다.

## 데이터 모델과 저장소

포인트 잔액을 저장하려면 영속적인 저장소가 필요합니다. SQLite, PostgreSQL,
Redis 등 다양한 DB를 사용할 수 있으며, `aiosqlite`나 `asyncpg` 같은 비동기
라이브러리를 활용해 I/O를 논블로킹으로 수행합니다. 테이블 구조는 간단하게
`(user_id INTEGER PRIMARY KEY, balance INTEGER)` 형식으로 설계할 수 있습니다.

```sql
CREATE TABLE IF NOT EXISTS balances (
    user_id INTEGER PRIMARY KEY,
    balance INTEGER NOT NULL DEFAULT 0
);
```

## 포인트 지급 및 조회

봇 명령이나 이벤트 핸들러에서 포인트를 지급할 때는 **트랜잭션**과
동시성 제어가 필요합니다. 예를 들어 여러 사용자가 동시에 포인트를 얻는 경우
DB 업데이트가 꼬이지 않도록 `asyncio.Lock`으로 보호하거나, 데이터베이스의
`BEGIN`/`COMMIT` 트랜잭션을 사용합니다.

```python
import aiosqlite

class Economy:
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.lock = asyncio.Lock()

    async def init_db(self):
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                "CREATE TABLE IF NOT EXISTS balances (user_id INTEGER PRIMARY KEY, balance INTEGER NOT NULL DEFAULT 0)"
            )
            await db.commit()

    async def add_points(self, user_id: int, amount: int):
        async with self.lock:
            async with aiosqlite.connect(self.db_path) as db:
                await db.execute("INSERT INTO balances(user_id, balance) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET balance = balance + ?", (user_id, amount, amount))
                await db.commit()

    async def get_balance(self, user_id: int) -> int:
        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute("SELECT balance FROM balances WHERE user_id = ?", (user_id,)) as cursor:
                row = await cursor.fetchone()
                return row[0] if row else 0
```

## 명령과 일일 보상

포인트 시스템을 제공하는 Cog를 만들고, `!balance`, `!daily`, `!give` 등 명령을
정의합니다. 일일 보상은 `tasks.loop` 데코레이터를 사용하여 24시간마다 자동으로
지급할 수 있습니다【230406618874054†L160-L210】. 사용자가 명령을 실행할 때는
해당 사용자의 포인트 잔액을 조회하고 업데이트합니다.

```python
class EconomyCog(commands.Cog):
    def __init__(self, bot, economy):
        self.bot = bot
        self.economy = economy
        self.daily_reward = 100
        self.claimed: set[int] = set()
        self.reward_loop.start()

    @commands.command(name="balance")
    async def balance(self, ctx):
        bal = await self.economy.get_balance(ctx.author.id)
        await ctx.send(f"{ctx.author.display_name}님의 잔액: {bal} 코인")

    @commands.command(name="give")
    async def give(self, ctx, member: discord.Member, amount: int):
        await self.economy.add_points(ctx.author.id, -amount)
        await self.economy.add_points(member.id, amount)
        await ctx.send(f"{ctx.author.display_name} → {member.display_name} : {amount} 코인을 전송했습니다.")

    @tasks.loop(hours=24)
    async def reward_loop(self):
        self.claimed.clear()

    @commands.command(name="daily")
    async def daily(self, ctx):
        if ctx.author.id in self.claimed:
            return await ctx.send("이미 오늘의 보상을 받았습니다!")
        await self.economy.add_points(ctx.author.id, self.daily_reward)
        self.claimed.add(ctx.author.id)
        await ctx.send(f"{self.daily_reward} 코인을 지급했습니다. 내일 다시 찾아주세요!")

    @reward_loop.before_loop
    async def before_reward(self):
        await self.bot.wait_until_ready()
```

위 예제에서 `reward_loop`는 24시간마다 `claimed` 집합을 초기화하여 사용자가
다시 일일 보상을 받을 수 있도록 합니다. 실제 서비스에서는 사용자의 시간대를
고려하거나 더 세밀한 간격으로 보상할 수 있습니다.

## 상점과 역할 구매

포인트로 구매할 수 있는 **상점** 기능도 구현할 수 있습니다. 예를 들어 특정
역할을 포인트로 판매하여 멤버에게 특수 권한을 부여하거나, 이모티콘과 닉네임
변경권 등을 판매할 수 있습니다. 데이터베이스에 아이템 목록과 가격을 저장하고
`!shop` 명령을 통해 사용자에게 목록을 보여준 뒤, `!buy <item>` 명령으로
포인트를 차감하고 권한을 부여합니다. 권한 부여는 `discord.Member.add_roles()`
메서드로 수행합니다.

포인트와 아이템 가격은 서버 규모와 경제 인플레이션을 고려해 적절히 조정해야
하며, 부정행위 방지를 위해 지급 로직을 서버 이벤트에 맞게 조정해야 합니다.

---

포인트 시스템은 커뮤니티 참여를 독려하는 강력한 도구입니다. 위의 구조를
참고하여 자신만의 경제를 설계해 보세요.