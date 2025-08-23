# 39장 – 음성 채널과 오디오 재생

디스코드 봇은 음성 채널에 참여하여 음악이나 음성 파일을 재생할 수 있습니다. `discord.py`는 음성 기능을 별도 의존성으로 분리했으므로, 사용하려면 설치 시 `[voice]` 옵션을 포함해야 합니다 (`pip install -U discord.py[voice]`). 이 장에서는 음성 채널에 연결하고, 로컬 파일이나 스트림을 재생하는 기본적인 방법을 소개합니다.

## 음성 채널 연결

봇이 음성 채널에 참여하려면 해당 길드의 음성 권한이 필요합니다. `voice_channel.connect()` 메서드를 사용해 `VoiceClient` 인스턴스를 얻을 수 있으며, 이미 연결되어 있다면 `move_to()`로 채널을 이동할 수 있습니다.

```python
@bot.command()
async def join(ctx):
    if ctx.author.voice is None:
        await ctx.send("음성 채널에 먼저 접속해 주세요.")
        return
    channel = ctx.author.voice.channel
    await channel.connect()
    await ctx.send(f"{channel.name} 채널에 연결되었습니다.")
```

## 오디오 재생

`FFmpegPCMAudio` 또는 `PCMVolumeTransformer` 클래스를 사용해 로컬 파일이나 스트림을 재생할 수 있습니다. FFmpeg가 서버에 설치되어 있어야 하며, 파일 경로나 URL을 지정할 수 있습니다. 다음은 로컬 MP3 파일을 재생하는 예제입니다.

```python
@bot.command()
async def play(ctx, *, filename: str):
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if not voice or not voice.is_connected():
        await ctx.send("먼저 음성 채널에 연결해야 합니다.")
        return
    source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(source=filename))
    voice.play(source)
    await ctx.send(f"재생 중: {filename}")
```

또는 YouTube URL과 같은 스트림을 직접 재생할 수도 있지만, 저작권 문제와 라이브러리 의존성(예: `youtube_dl`나 `yt-dlp`)을 고려해야 합니다.

## 연결 해제 및 정리

재생이 끝난 후 봇이 채널에 계속 남아 있지 않도록 `VoiceClient.disconnect()`를 호출해 연결을 끊어야 합니다. 또한 오류 발생 시 `voice.stop()`으로 재생을 중단하고, 필요한 경우 `after` 콜백에서 자동으로 다음 트랙을 재생하도록 구현할 수 있습니다.

## 요약

음성 기능은 봇에 풍성한 경험을 더해 줍니다. 음성 채널에 연결하려면 사용자가 먼저 채널에 있어야 하며, `discord.py` 설치 시 `[voice]` 옵션을 활성화해야 합니다. FFmpeg를 사용해 로컬 파일이나 스트림을 재생하고, 재생이 끝나면 적절히 연결을 끊어 리소스를 관리하세요.

