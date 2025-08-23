"""권한과 역할 관리 예제.

봇 명령에 필요한 권한을 지정하고, 역할을 부여/제거하는 방법을 보여 줍니다.
"""

import discord
from discord.ext import commands


bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())


# 메시지 관리 권한이 있는 사용자만 사용 가능한 명령어
@bot.command()
@commands.has_permissions(manage_messages=True)
async def purge(ctx: commands.Context, limit: int = 5) -> None:
    """최근 메시지를 삭제합니다."""
    await ctx.channel.purge(limit=limit)
    await ctx.send(f"{limit}개의 메시지를 삭제했습니다.")


# 특정 역할을 가진 사용자만 사용 가능한 명령어
@bot.command()
@commands.has_any_role("관리자", "모더레이터")
async def announce(ctx: commands.Context, *, message: str) -> None:
    """공지 메시지를 출력합니다."""
    await ctx.send(f"📢 {message}")


# 역할을 부여하는 명령어: 봇에게 manage_roles 권한이 필요합니다.
@bot.command(name="가입")
@commands.has_permissions(manage_roles=True)
async def assign_role(ctx: commands.Context, member: discord.Member, role: discord.Role) -> None:
    await member.add_roles(role)
    await ctx.send(f"{member.display_name}님에게 {role.name} 역할을 부여했습니다.")


@assign_role.error
async def assign_role_error(ctx: commands.Context, error: commands.CommandError) -> None:
    if isinstance(error, commands.BadArgument):
        await ctx.send("사용자나 역할을 정확히 멘션해 주세요.")
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send("역할을 부여할 권한이 없습니다.")


if __name__ == "__main__":
    # bot.run("YOUR_TOKEN")
    pass