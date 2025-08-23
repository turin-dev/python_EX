"""임베드 예제.

서버의 정보를 임베드 형식으로 출력하는 명령어를 구현합니다.
"""

import discord
from discord.ext import commands


bot = commands.Bot(command_prefix="!", intents=discord.Intents.default())


@bot.command(name="서버정보")
async def server_info(ctx: commands.Context) -> None:
    """현재 서버의 정보를 임베드로 보냅니다."""
    guild = ctx.guild
    embed = discord.Embed(
        title=f"{guild.name} 서버 정보",
        description=f"멤버 수: {guild.member_count}",
        color=discord.Color.green(),
    )
    # 썸네일 설정 (서버 아이콘이 존재할 경우)
    if guild.icon:
        embed.set_thumbnail(url=guild.icon.url)
    embed.add_field(name="서버 ID", value=str(guild.id), inline=False)
    embed.add_field(name="채널 수", value=str(len(guild.channels)), inline=True)
    embed.add_field(name="역할 수", value=str(len(guild.roles)), inline=True)
    embed.set_footer(text=f"요청자: {ctx.author.display_name}")
    await ctx.send(embed=embed)


if __name__ == "__main__":
    # bot.run("YOUR_TOKEN")
    pass