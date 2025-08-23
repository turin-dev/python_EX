"""음성 채널 예제.

음성 채널에 연결하고 로컬 오디오 파일을 재생하는 명령어를 구현합니다. FFmpeg가 설치되어 있어야 합니다.
"""

import discord
from discord.ext import commands


bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())


@bot.command(name="join")
async def join_voice(ctx: commands.Context) -> None:
    """사용자의 음성 채널에 봇을 연결합니다."""
    if ctx.author.voice is None:
        await ctx.send("먼저 음성 채널에 접속해 주세요.")
        return
    channel = ctx.author.voice.channel
    await channel.connect()
    await ctx.send(f"{channel.name} 채널에 연결되었습니다.")


@bot.command(name="play")
async def play_audio(ctx: commands.Context, *, filename: str) -> None:
    """음성 채널에서 오디오 파일을 재생합니다."""
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if not voice or not voice.is_connected():
        await ctx.send("봇이 음성 채널에 연결되어 있지 않습니다. 먼저 `!join` 명령을 사용하세요.")
        return
    source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(source=filename))
    voice.play(source, after=lambda e: print(f"오디오 재생 종료: {e}" if e else "오디오 재생 완료"))
    await ctx.send(f"재생 중: {filename}")


@bot.command(name="leave")
async def leave_voice(ctx: commands.Context) -> None:
    """음성 채널 연결을 종료합니다."""
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if voice and voice.is_connected():
        await voice.disconnect()
        await ctx.send("음성 채널에서 퇴장했습니다.")
    else:
        await ctx.send("음성 채널에 연결되어 있지 않습니다.")


if __name__ == "__main__":
    # bot.run("YOUR_TOKEN")
    pass