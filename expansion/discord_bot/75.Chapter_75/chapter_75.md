# 고급 스팸 방지와 보안

활발한 서버에서 봇은 스팸과 악용을 방지해야 합니다. 단순한 욕설 필터를 넘어서
대량 멘션, 도배 메시지, 의심스러운 링크 등 다양한 위협을 탐지하고 차단하는
로직이 필요합니다. 또한 봇 자체의 보안도 중요합니다. 토큰 유출과 권한 남용을
막고, Discord API의 권장 사항을 준수해야 합니다. 이 장에서는 고급 스팸
방지 기법과 보안 모범 사례를 설명합니다.

## 스팸 패턴 탐지

### 속도 기반 감지
사용자가 짧은 시간에 많은 메시지를 보내면 스팸일 가능성이 큽니다. 사용자별로
최근 메시지 타임스탬프를 저장하고 간격이 너무 짧으면 경고하거나 침묵 처리합니다.

```python
class AntiSpam(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.timestamps: dict[int, list[float]] = {}
        self.limit = 5  # 5초 내 5회 이상은 스팸으로 간주

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        now = message.created_at.timestamp()
        times = self.timestamps.setdefault(message.author.id, [])
        times.append(now)
        # 최근 5초의 기록만 유지
        times[:] = [t for t in times if now - t < 5]
        if len(times) > self.limit:
            await message.delete()
            await message.channel.send(f"{message.author.mention}, 메시지를 너무 빠르게 보냅니다. 잠시 휴식하세요.")
```

### 멘션/링크 스팸
`message.mentions`와 `message.role_mentions` 길이를 검사하여, 한 메시지에
허용된 수를 넘는 멘션이 있으면 삭제합니다. 의심스러운 링크(예: 디스코드 초대
링크, 피싱 URL) 목록을 유지하여 차단할 수도 있습니다.

```python
MAX_MENTIONS = 5
BLOCKED_DOMAINS = {"phish.example", "scam.com"}

@bot.event
async def on_message(message):
    if len(message.mentions) + len(message.role_mentions) > MAX_MENTIONS:
        await message.delete()
        await message.channel.send(f"@멘션을 너무 많이 사용했습니다.", delete_after=5)
    for word in message.content.split():
        if any(domain in word for domain in BLOCKED_DOMAINS):
            await message.delete()
            break
    await bot.process_commands(message)
```

### 첨부파일 검사
첨부파일은 악성 코드나 음란물을 포함할 수 있습니다. 봇은 파일의 MIME 유형과
크기를 검사하여 허용된 목록에 없는 경우 삭제하고 경고합니다. 더 나아가서는
클램AV(ClamAV)와 같은 바이러스 검사 API를 연동해 파일을 스캔할 수 있습니다.

```python
ALLOWED_MIME = {"image/png", "image/jpeg", "image/gif"}
MAX_SIZE = 8 * 1024 * 1024  # 8MB

@bot.event
async def on_message(message):
    for attachment in message.attachments:
        if attachment.size > MAX_SIZE or (attachment.content_type and attachment.content_type not in ALLOWED_MIME):
            await attachment.delete()
            await message.channel.send(f"허용되지 않는 첨부파일이 삭제되었습니다.", delete_after=5)
            return
    await bot.process_commands(message)
```

## 권한과 Mentions 제어

디스코드 메시지를 보낼 때 기본적으로 `@everyone`이나 `@here`를 멘션할 수 있습니다.
하지만 봇이 이를 무분별하게 사용하면 서버를 혼란에 빠뜨릴 수 있습니다. 메시지를
보낼 때는 `allowed_mentions` 매개변수를 활용해 허용된 멘션 유형을 제한하세요.
예를 들어 모든 역할과 `@everyone` 멘션을 비활성화하고, 사용자 멘션만 허용할
수 있습니다:

```python
allowed = discord.AllowedMentions(everyone=False, roles=False, users=True)
await channel.send("안전한 멘션", allowed_mentions=allowed)
```

또한 명령어 실행 시 `@commands.has_permissions()` 데코레이터를 사용해 관리자가
아닌 사용자의 중요 명령 접근을 막고, `dm_only` 또는 `guild_only` 체크로 명령의
사용 위치를 제한합니다. 적절한 인텐트를 설정해 필요한 이벤트만 수신하고
불필요한 정보 노출을 최소화해야 합니다【666664033931420†L32-L45】.

## 토큰 보안과 환경 분리

- **토큰 노출 방지**: 봇의 토큰은 절대로 코드 저장소에 커밋하면 안 됩니다. `.env` 파일이나 환경 변수에 저장하고 `os.getenv()`로 읽어옵니다.
- **권한 최소화**: 초대 URL 생성 시 최소한의 권한만 부여합니다. 특히 `administrator` 권한은 정말 필요할 때만 사용하고, 권한을 명령별로 세분화합니다.
- **로그 관리**: 감시 채널에 중요한 명령 실행 기록과 오류 스택 트레이스를 로그로 남기고, 민감한 정보(토큰, API 키)는 로깅하지 않습니다.

---

이 장에서 소개한 스팸 방지 패턴과 보안 기법을 통해 서버를 안전하게 유지하고 봇이 악용되는 일을 방지할 수 있습니다.