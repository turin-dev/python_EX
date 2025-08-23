"""
음성 채널과 음악 재생 예제.

이 스크립트는 `discord.py[voice]` 확장을 사용하여 음성 채널에 접속하고,
로컬 오디오 파일이나 YouTube 스트림을 재생하는 방법을 보여줍니다. 실제
운영 환경에서는 `pip install -U discord.py[voice] yt-dlp` 등을 통해
필수 의존성을 설치해야 합니다.

명령:
  - `!join`: 호출자의 음성 채널에 봇을 참가시킴
  - `!play <filename>`: media 폴더의 파일 재생
  - `!yt <url>`: YouTube URL에서 오디오 스트림 추출 후 재생
  - `!stop`: 현재 재생 중지 및 음성 채널 나가기
"""

import asyncio
import os
import discord
from discord.ext import commands

try:
    import yt_dlp  # YouTube 다운로드 도구
except ImportError:
    yt_dlp = None


bot = commands.Bot(command_prefix="!", intents=discord.Intents.default())


@bot.command(name="join")
async def join(ctx: commands.Context) -> None:
    """사용자가 있는 음성 채널에 참가합니다."""
    if not ctx.author.voice:
        return await ctx.send("먼저 음성 채널에 접속한 뒤 명령을 실행하세요.")
    channel = ctx.author.voice.channel
    if ctx.voice_client:
        await ctx.voice_client.move_to(channel)
    else:
        await channel.connect()
    await ctx.send(f"음성 채널 `{channel.name}`에 접속했습니다.")


@bot.command(name="play")
async def play(ctx: commands.Context, *, filename: str) -> None:
    """media 디렉터리의 파일을 재생합니다."""
    if not ctx.author.voice:
        return await ctx.send("음성 채널에 먼저 접속하세요.")
    # 연결이 없다면 연결
    voice_client: discord.VoiceClient = ctx.voice_client or await ctx.author.voice.channel.connect()
    # 기존 재생 중지
    if voice_client.is_playing():
        voice_client.stop()
    path = os.path.join("media", filename)
    if not os.path.exists(path):
        return await ctx.send("파일을 찾을 수 없습니다.")
    source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(path), volume=0.5)
    voice_client.play(source, after=lambda e: print(f"재생 오류: {e}" if e else "재생 완료"))
    await ctx.send(f"재생 시작: {filename}")


@bot.command(name="yt")
async def play_youtube(ctx: commands.Context, url: str) -> None:
    """YouTube 오디오 스트림을 재생합니다."""
    if yt_dlp is None:
        return await ctx.send("yt-dlp 라이브러리가 설치되어 있지 않습니다.")
    if not ctx.author.voice:
        return await ctx.send("음성 채널에 먼저 접속하세요.")
    voice_client: discord.VoiceClient = ctx.voice_client or await ctx.author.voice.channel.connect()
    # 재생 중이면 중지
    if voice_client.is_playing():
        voice_client.stop()
    def get_stream() -> tuple[str, str]:
        # blocking 작업: yt_dlp로 스트림 URL 추출
        with yt_dlp.YoutubeDL({"format": "bestaudio"}) as ydl:
            info = ydl.extract_info(url, download=False)
            return info["url"], info.get("title", url)
    stream_url, title = await asyncio.to_thread(get_stream)
    source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(stream_url), volume=0.5)
    voice_client.play(source, after=lambda e: print(f"스트림 오류: {e}" if e else "스트림 종료"))
    await ctx.send(f"유튜브 스트림 재생 중: {title}")


@bot.command(name="stop")
async def stop(ctx: commands.Context) -> None:
    """현재 재생을 중지하고 음성 채널을 나갑니다."""
    if not ctx.voice_client:
        return await ctx.send("봇이 음성 채널에 있지 않습니다.")
    ctx.voice_client.stop()
    await ctx.voice_client.disconnect()
    await ctx.send("재생을 중지하고 음성 채널에서 나왔습니다.")


if __name__ == "__main__":
    token = os.getenv("DISCORD_TOKEN")
    if not token:
        raise RuntimeError("DISCORD_TOKEN 환경 변수가 설정되지 않았습니다.")
    bot.run(token)