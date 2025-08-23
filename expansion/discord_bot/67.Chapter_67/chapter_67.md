# 커맨드 카테고리와 도움말 커스터마이징

봇이 여러 명령어를 제공하다 보면 사용자에게 명령어를 보기 좋게 분류하고 설명하는 것이 필요합니다. `discord.py`의 `commands.HelpCommand` 클래스를 상속하거나 대체하여 도움말 메시지를 커스터마이징할 수 있습니다. 또한 명령을 Cog별로 분류하여 카테고리를 만들고, 도움말에 카테고리 헤더를 넣을 수 있습니다.

## Cog를 통한 카테고리화

명령어를 `commands.Cog` 클래스 내에 정의하면 Cog 이름이 곧 카테고리 이름으로 사용됩니다. Cog 클래스에 `description` 속성을 설정하면 도움말 페이지에 간단한 설명을 표시할 수 있습니다. 예를 들어:

```python
class UtilityCog(commands.Cog, name="유틸리티", description="유용한 일반 명령 모음"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="핑")
    async def ping(self, ctx):
        """봇 지연 시간을 확인합니다."""
        await ctx.send(f"Pong! {round(self.bot.latency * 1000)}ms")
```

이 Cog를 등록하면, 기본 도움말에서 "유틸리티" 카테고리 아래에 `핑` 명령이 표시됩니다.

## 도움말 명령 커스터마이징

기본 도움말(`Bot.help_command`)은 모든 Cog와 명령을 나열하지만, 포맷을 수정하거나 특정 명령을 숨기려면 커스텀 헬프 명령을 구현할 수 있습니다. `commands.MinimalHelpCommand`는 간단한 텍스트 기반 도움말을 생성하며, 이를 상속하여 포맷을 변경할 수 있습니다. 다음은 명령 리스트를 이모지와 함께 나열하는 예제입니다:

```python
class MyHelpCommand(commands.MinimalHelpCommand):
    def get_command_signature(self, command):
        return f"{self.clean_prefix}{command.qualified_name} {command.signature}"

    async def send_bot_help(self, mapping):
        embed = discord.Embed(title="도움말", color=0x00BFFF)
        for cog, commands_ in mapping.items():
            filtered = await self.filter_commands(commands_, sort=True)
            if not filtered:
                continue
            name = cog.qualified_name if cog else "기타"
            value = "\n".join(f"• {self.get_command_signature(c)}" for c in filtered)
            embed.add_field(name=name, value=value, inline=False)
        channel = self.get_destination()
        await channel.send(embed=embed)

bot.help_command = MyHelpCommand()
```

위 커스텀 도움말은 각 Cog 이름을 제목으로 하고, 명령을 목록 형식으로 나열합니다. `filter_commands`는 권한이나 체크에 따라 볼 수 있는 명령만 포함시킵니다. 필요에 따라 `send_cog_help`나 `send_command_help`를 오버라이드하여 세부 페이지를 꾸밀 수 있습니다.

## 요약

Cog로 명령을 조직하면 카테고리별로 명령을 관리할 수 있으며, `HelpCommand`를 오버라이드하면 봇의 성격에 맞는 도움말 인터페이스를 제공할 수 있습니다. 사용자 친화적인 도움말은 봇의 접근성을 높이고 사용자가 기능을 쉽게 찾을 수 있게 해 줍니다.

