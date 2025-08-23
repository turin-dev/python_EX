"""
여러 길드 기능 예제.

이 모듈에는 다음과 같은 기능이 구현되어 있습니다.

1. 글로벌 리더보드: SQLite 데이터베이스에서 모든 사용자 잔액을 합산하여
   상위 10명을 보여줍니다.
2. 메시지 브리지: 한 채널에서 보낸 메시지를 다른 채널들로 복제하는 브리지.

사전 준비: EconomyDB 또는 비슷한 저장소가 `fetch_all` 메서드를 제공해야 하고,
봇에 필요한 권한(웹훅 관리, 메시지 관리)이 있어야 합니다.
"""

from __future__ import annotations
import discord
from discord.ext import commands

from typing import List, Dict


class LeaderboardCog(commands.Cog):
    def __init__(self, bot: commands.Bot, db) -> None:
        self.bot = bot
        self.db = db  # EconomyDB 같은 객체

    @commands.command(name="leaderboard")
    async def leaderboard(self, ctx: commands.Context) -> None:
        """포인트 기준 글로벌 상위 10명을 보여줍니다."""
        # 예시: db.fetch_all()은 rows를 반환하는 가정
        rows = await self.db.fetch_all(
            "SELECT user_id, SUM(balance) AS total FROM balances GROUP BY user_id ORDER BY total DESC LIMIT 10"
        )
        if not rows:
            return await ctx.send("리더보드 데이터가 없습니다.")
        desc_lines = []
        for i, row in enumerate(rows, start=1):
            user_id = row[0] if isinstance(row, (list, tuple)) else row["user_id"]
            total = row[1] if isinstance(row, (list, tuple)) else row["total"]
            # 사용자 이름 가져오기 (캐싱하면 더 효율적)
            member = ctx.guild.get_member(user_id) or (await self.bot.fetch_user(user_id))
            name = member.display_name if hasattr(member, "display_name") else str(user_id)
            desc_lines.append(f"{i}. {name}: {total} 코인")
        embed = discord.Embed(title="글로벌 리더보드", description="\n".join(desc_lines), color=discord.Color.gold())
        await ctx.send(embed=embed)


class BridgeCog(commands.Cog):
    """특정 채널에서 다른 채널들로 메시지를 릴레이하는 브리지."""
    def __init__(self, bot: commands.Bot, source_channel_id: int, dest_channel_ids: List[int]):
        self.bot = bot
        self.source_channel_id = source_channel_id
        self.dest_channel_ids = dest_channel_ids
        self.webhooks: Dict[int, discord.Webhook] = {}

    async def get_webhook(self, channel: discord.TextChannel) -> discord.Webhook:
        if channel.id in self.webhooks:
            return self.webhooks[channel.id]
        hooks = await channel.webhooks()
        if hooks:
            hook = hooks[0]
        else:
            hook = await channel.create_webhook(name="Relay")
        self.webhooks[channel.id] = hook
        return hook

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message) -> None:
        if message.author.bot or message.channel.id != self.source_channel_id:
            return
        for dest_id in self.dest_channel_ids:
            dest = self.bot.get_channel(dest_id)
            if not isinstance(dest, discord.TextChannel):
                continue
            hook = await self.get_webhook(dest)
            await hook.send(
                content=message.content,
                username=message.author.display_name,
                avatar_url=message.author.display_avatar.url,
                allowed_mentions=discord.AllowedMentions.none(),
            )


async def setup(bot: commands.Bot) -> None:
    # db는 이전 장의 EconomyDB 또는 fetch_all()을 제공하는 다른 객체
    # 실제 등록 시 bot instance에 저장하거나 파라미터로 전달해야 함
    # 여기서는 더미 구현으로 전달되지 않음
    pass