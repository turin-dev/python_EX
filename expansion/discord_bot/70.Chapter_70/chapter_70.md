# 음성 채널과 음악 재생

텍스트 명령과 슬래시 명령만으로는 표현에 한계가 있습니다. 음성 채널에 접속해
음악을 틀거나 알림을 녹음으로 재생하면 봇의 활용도가 크게 넓어집니다. 하지만
음성 관련 기능은 **추가 의존성**과 적절한 오류 처리, 그리고 Discord의 인텐트
설정이 필요합니다. 이 장에서는 `discord.py`를 사용해 음성 채널에 연결하고
오디오를 재생하는 방법을 자세히 설명합니다. 기본 음성 연결은 일반 클라이언트
인텐트로 가능하지만, 봇이 특정 음성 이벤트를 감지하려면 `Intents.voice_states`
등을 활성화해야 합니다【666664033931420†L32-L45】.

## 환경 설정과 의존성

- **`discord.py[voice]` extras**: 음성 기능을 사용하려면 `pip install discord.py[voice]`로 opus 및 ffmpeg/avlib 지원이 포함된 확장 설치가 필요합니다. 시스템에 FFmpeg가 설치돼 있어야 합니다.
- **FFmpeg**: 오디오 파일 또는 스트림을 PCM 데이터로 변환합니다. 대부분의 배포 환경에서 패키지 매니저로 설치할 수 있습니다(예: `apt install ffmpeg`).

## 음성 채널 연결

음성 채널에 참가하려면 `Member.voice.channel`을 통해 사용자가 있는 채널을 가져오거나 `Guild.voice_channels` 리스트에서 적절한 채널을 선택합니다. 그리고 `voice_client = await channel.connect()`로 연결을 생성합니다. 이미 연결된 경우 `guild.voice_client`를 사용하면 기존 연결을 재사용할 수 있습니다.

```python
@bot.command(name="join")
async def join_channel(ctx):
    # 사용자가 음성 채널에 있는지 확인
    if not ctx.author.voice:
        return await ctx.send("먼저 음성 채널에 접속하세요.")
    channel = ctx.author.voice.channel
    # 이미 다른 채널에 연결돼 있으면 이동
    if ctx.voice_client:
        await ctx.voice_client.move_to(channel)
    else:
        await channel.connect()
    await ctx.send(f"{channel.name} 채널에 접속했습니다.")
```

## 로컬 파일 재생

음성 연결 후에는 `discord.FFmpegPCMAudio`를 이용해 로컬 파일을 재생할 수 있습니다. PCM 스트림은 `source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio('song.mp3'), volume=0.5)`처럼 볼륨을 조절할 수도 있습니다. 재생이 끝나면 콜백을 통해 자동으로 다음 곡을 재생하거나 연결을 끊을 수 있습니다.

```python
@bot.command(name="play")
async def play_audio(ctx, *, filename: str):
    if not ctx.author.voice:
        return await ctx.send("음성 채널에 먼저 접속하세요.")
    if not ctx.voice_client:
        await ctx.author.voice.channel.connect()
    # 재생 중이면 먼저 중지
    if ctx.voice_client.is_playing():
        ctx.voice_client.stop()
    source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(f"media/{filename}"), volume=0.6)
    ctx.voice_client.play(source, after=lambda e: print(f"재생 종료: {e}"))
    await ctx.send(f"재생 중: {filename}")
```

## YouTube 및 스트리밍 재생

YouTube나 인터넷 스트림을 재생하려면 `youtube-dl`이나 `yt-dlp`를 통해 오디오 스트림 URL을 추출하고 FFmpeg로 변환해야 합니다. 비동기 환경에서는 `yt_dlp.YoutubeDL`을 `asyncio.to_thread`로 감싸 blocking I/O를 분리합니다. 예시:

```python
import yt_dlp

@bot.command(name="yt")
async def play_youtube(ctx, url: str):
    if not ctx.author.voice:
        return await ctx.send("음성 채널에 먼저 접속하세요.")
    vc = ctx.voice_client or await ctx.author.voice.channel.connect()
    # YouTube 스트림 URL 추출 (차단적 작업)
    def get_source():
        with yt_dlp.YoutubeDL({'format': 'bestaudio'}) as ydl:
            info = ydl.extract_info(url, download=False)
            return info['url']
    stream_url = await asyncio.to_thread(get_source)
    source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(stream_url), volume=0.5)
    vc.play(source)
    await ctx.send(f"재생 중: {info['title']}")
```

## 음성 상태 이벤트 처리

봇이 음성 채널에서 재생을 제어하려면 `on_voice_state_update` 이벤트를 활용할 수 있습니다. 예를 들어 사용자가 채널을 떠날 때 자동으로 재생을 중지하거나, 봇이 혼자 남으면 채널을 떠나도록 할 수 있습니다. 또한 봇의 음량을 조절하는 명령, 재생 중지/일시정지/다시재생 등의 명령을 구현해 사용자 경험을 개선합니다.

```python
@bot.event
async def on_voice_state_update(member, before, after):
    # 봇의 음성 클라이언트가 존재하고, 봇만 남았을 때 연결 끊기
    if member == ctx.guild.me and after.channel is None and ctx.voice_client:
        await ctx.voice_client.disconnect()
```

## 정리

음성 기능을 구현할 때는 외부 라이브러리와 시스템 종속성이 필요하므로 개발 환경을 신중히 준비해야 합니다. 또한 음성 채널 연결은 네트워크 상태에 민감하여 예외 처리를 꼼꼼히 작성해야 합니다. 본 장의 예제 코드를 기반으로 MP3 재생, 유튜브 스트림 재생, 음량 조절, 음성 이벤트 처리 등을 응용해 보세요.

---

> **참고:** 인텐트 설정 및 권한 구성에 대한 자세한 내용은 인텐트 기본 장을 참고하세요【666664033931420†L32-L45】.