"""
고급 스팸 방지와 보안 예제.

이 모듈은 메시지 속도 제한, 멘션/링크 스팸 필터, 첨부파일 검사, 안전한
멘션 전송을 구현한 예제입니다. AntiSpamCog는 사용자별 메시지 발송 속도를
추적하여 도배를 감지하고, 불량 링크와 과도한 멘션을 차단합니다.

설정 값은 클래스 상단의 상수로 정의되어 있으며, 상황에 맞게 조절해야 합니다.
"""

from __future__ import annotations
import asyncio
import time
from typing import Dict, List, Set

import discord
from discord.ext import commands


ALLOWED_MENTION = discord.AllowedMentions(everyone=False, roles=False, users=True)
MAX_MESSAGES_PER_WINDOW = 5
WINDOW_SECONDS = 5
MAX_MENTIONS = 5
BLOCKED_DOMAINS = {"phishing.example", "malware.com", "scam.net"}
ALLOWED_MIME = {"image/png", "image/jpeg", "image/gif"}
MAX_ATTACHMENT_SIZE = 8 * 1024 * 1024  # 8MB


class AntiSpamCog(commands.Cog):
    """스팸 메시지와 악성 컨텐츠를 감지하는 Cog."""
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        # user_id -> [timestamps]
        self.history: Dict[int, List[float]] = {}

    def _check_speed(self, user_id: int) -> bool:
        now = time.monotonic()
        timestamps = self.history.setdefault(user_id, [])
        timestamps.append(now)
        # 최근 WINDOW_SECONDS 초의 기록만 남김
        self.history[user_id] = [t for t in timestamps if now - t <= WINDOW_SECONDS]
        return len(self.history[user_id]) > MAX_MESSAGES_PER_WINDOW

    async def _check_links(self, content: str) -> bool:
        for token in content.split():
            for domain in BLOCKED_DOMAINS:
                if domain in token:
                    return True
        return False

    async def _check_attachments(self, message: discord.Message) -> bool:
        for att in message.attachments:
            if att.size > MAX_ATTACHMENT_SIZE:
                return True
            if att.content_type and att.content_type not in ALLOWED_MIME:
                return True
        return False

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message) -> None:
        # 봇 메시지는 무시
        if message.author.bot:
            return
        # 첨부파일 검사
        if await self._check_attachments(message):
            await message.delete()
            await message.channel.send(
                f"{message.author.mention}, 허용되지 않는 첨부파일이 삭제되었습니다.",
                delete_after=5,
            )
            return
        # 속도 스팸 검사
        if self._check_speed(message.author.id):
            await message.delete()
            await message.channel.send(
                f"{message.author.mention}, 메시지를 너무 빠르게 보내고 있습니다. 잠시만요!",
                delete_after=5,
            )
            return
        # 링크 검사
        if await self._check_links(message.content):
            await message.delete()
            await message.channel.send(
                f"{message.author.mention}, 허용되지 않는 링크가 포함되어 있어 메시지가 삭제되었습니다.",
                delete_after=5,
            )
            return
        # 멘션 수 검사
        if len(message.mentions) + len(message.role_mentions) > MAX_MENTIONS:
            await message.delete()
            await message.channel.send(
                f"{message.author.mention}, 멘션이 너무 많습니다. 최대 {MAX_MENTIONS}개까지 허용됩니다.",
                delete_after=5,
            )
            return
        # 통과: 명령 처리 계속
        await self.bot.process_commands(message)

    @commands.command(name="announce")
    @commands.has_permissions(manage_guild=True)
    async def announce(self, ctx: commands.Context, *, content: str) -> None:
        """안전한 멘션 설정을 사용하여 공지 메시지를 보냅니다."""
        await ctx.send(content, allowed_mentions=ALLOWED_MENTION)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(AntiSpamCog(bot))