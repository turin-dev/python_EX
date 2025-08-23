"""하이브리드 명령과 명령 그룹 예제.

이 모듈은 하나의 함수로 슬래시와 접두사 명령을 동시에 구현하는
하이브리드 명령과 하이브리드 명령 그룹의 예제를 제공합니다.
명령 그룹을 사용하면 관련 명령을 묶어 사용자에게 논리적인
트리를 제공할 수 있습니다.
"""

import discord
from discord.ext import commands


# 간단한 설정 저장소 (메모리상)
CONFIG: dict[str, str] = {}


def create_bot() -> commands.Bot:
    """하이브리드 명령을 포함한 Bot 인스턴스를 생성합니다."""
    intents = discord.Intents.default()
    intents.message_content = True  # 접두사 명령 처리를 위해 필요
    bot = commands.Bot(command_prefix="!", intents=intents)

    @bot.hybrid_command(name="hello", description="인사를 합니다")
    async def hello(ctx: commands.Context) -> None:
        await ctx.send(f"안녕하세요 {ctx.author.display_name}님!")

    @bot.hybrid_group(name="설정", description="봇 설정 명령어 그룹")
    async def config(ctx: commands.Context) -> None:
        if not ctx.invoked_subcommand:
            await ctx.send("사용 가능한 서브커맨드: 조회, 변경")

    @config.command(name="조회")
    async def config_get(ctx: commands.Context, key: str) -> None:
        value = CONFIG.get(key, "설정되지 않음")
        await ctx.send(f"{key} = {value}")

    @config.command(name="변경")
    async def config_set(ctx: commands.Context, key: str, value: str) -> None:
        CONFIG[key] = value
        await ctx.send(f"{key}가 {value}로 설정되었습니다")

    return bot


if __name__ == "__main__":
    bot = create_bot()

    @bot.event
    async def on_ready() -> None:
        print(f"Logged in as {bot.user}")
        # 슬래시 명령을 동기화 (개발 중 특정 길드에만 동기화 가능)
        try:
            await bot.tree.sync()
        except Exception as e:
            print("Slash sync error", e)

    # 실제 실행 시 토큰을 환경 변수에서 불러옵니다.
    # bot.run(os.environ.get("DISCORD_TOKEN"))

