# 25장 – 임베드와 풍부한 메시지

평범한 텍스트 메시지 외에도 Discord는 제목, 설명, 이미지, 필드 등을 포함하는 **임베드(Embed)** 라는 구조화된 메시지를 지원합니다. 임베드를 사용하면 봇이 출력하는 정보를 시각적으로 돋보이게 만들 수 있습니다. `discord.Embed` 클래스를 활용하여 다양한 요소를 설정하는 방법을 익혀 봅시다.

## 기본 임베드 생성

임베드를 생성하려면 제목, 설명, 색상 등의 속성을 지정하고, 필요한 경우 썸네일이나 이미지, 작성자 정보를 추가합니다. 예를 들어 서버 정보 명령을 작성하면 다음과 같습니다.

```python
import discord
from discord.ext import commands

bot = commands.Bot(command_prefix="!")

@bot.command()
async def 서버정보(ctx):
    guild = ctx.guild
    embed = discord.Embed(
        title=f"{guild.name} 서버 정보",
        description=f"멤버 수: {guild.member_count}",
        color=discord.Color.blurple(),
    )
    embed.set_thumbnail(url=guild.icon.url if guild.icon else discord.Embed.Empty)
    embed.add_field(name="서버 ID", value=guild.id, inline=False)
    embed.add_field(name="채널 수", value=len(guild.channels), inline=True)
    embed.add_field(name="역할 수", value=len(guild.roles), inline=True)
    embed.set_footer(text=f"요청자: {ctx.author.display_name}")
    await ctx.send(embed=embed)
```

임베드의 색상은 `discord.Color` 열거형으로 지정하거나 16진수 정수(`0x3498DB`)를 사용할 수 있습니다. 텍스트의 길이는 Discord가 제한하므로, 제목은 256자, 설명은 4096자, 각 필드는 1024자 이하로 작성해야 합니다.

## 필드와 인라인 배치

`embed.add_field(name, value, inline)` 메서드를 사용하면 여러 필드를 추가할 수 있습니다. `inline=True`로 설정하면 필드가 같은 행에 최대 3개까지 나란히 표시되고, `inline=False`로 설정하면 새 행에 전체 너비로 나타납니다. 필드 이름 또는 값에 긴 문자열을 넣어야 할 때는 줄바꿈(`\n`)을 활용하여 가독성을 높입니다.

## 이미지와 미디어 추가

`embed.set_image(url)`로 본문 아래에 큰 이미지를 삽입하고, `set_thumbnail(url)`로 좌측 상단에 작은 이미지를 넣을 수 있습니다. 또한 `embed.set_author()`를 이용해 작성자 이름, 아이콘, 링크를 설정해 카드 형태로 표현할 수 있습니다. 사용자 아바타는 `ctx.author.avatar.url`로, 메시지 첨부 파일은 `attachment.url`로 얻을 수 있습니다.

## 요약

임베드를 활용하면 봇이 보내는 메시지를 더욱 풍부하고 읽기 쉽게 만들 수 있습니다. 제목, 설명, 필드, 이미지, 푸터 등 다양한 요소를 조합하여 정보를 구조화하고, 색상과 아이콘으로 브랜드를 표현해 보세요. 임베드 요소의 길이 제한과 Discord 클라이언트의 표시 방식에 주의해야 합니다.

