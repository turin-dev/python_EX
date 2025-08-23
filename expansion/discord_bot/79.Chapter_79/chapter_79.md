# 맞춤형 도움말과 메뉴 시스템

사용자가 명령을 쉽게 찾고 이해하도록 돕기 위해 봇의 **도움말 시스템**을
맞춤형으로 구현할 수 있습니다. 기본 `help` 명령은 모든 명령을 나열하지만,
카테고리별 정리나 인터랙티브 페이지가 없어서 보기가 힘들 수 있습니다.
이 장에서는 `HelpCommand` 클래스를 상속해 텍스트 기반 도움말을 재정의하는
방법과, 버튼 또는 셀렉트 메뉴를 사용해 메뉴 방식의 도움말을 제공하는
방법을 살펴봅니다.

## 커스텀 HelpCommand 작성

`discord.ext.commands.HelpCommand`를 상속해 `send_bot_help`, `send_cog_help`,
`send_command_help` 등을 오버라이드하면 명령 리스트를 원하는 형식으로 출력할
수 있습니다. 아래는 Cog별로 명령을 그룹화하고, 임베드로 표시하는 예제입니다.

```python
class EmbedHelpCommand(commands.MinimalHelpCommand):
    async def send_bot_help(self, mapping):
        embed = discord.Embed(title="도움말", description="사용 가능한 명령 목록")
        for cog, cmds in mapping.items():
            filtered = await self.filter_commands(cmds, sort=True)
            if not filtered:
                continue
            cog_name = getattr(cog, "qualified_name", "기타")
            cmd_list = ", ".join(cmd.name for cmd in filtered)
            embed.add_field(name=cog_name, value=cmd_list, inline=False)
        channel = self.get_destination()
        await channel.send(embed=embed)

bot = commands.Bot(command_prefix="!", help_command=EmbedHelpCommand())
```

`MinimalHelpCommand`는 기본 `HelpCommand`보다 구현할 메서드가 적어 간단합니다. 필요에 따라 특정 Cog나 명령에 대한 도움말 출력만 커스터마이징할 수 있습니다.

## 인터랙티브 도움말 메뉴

임베드와 버튼을 결합하여 사용자 친화적인 도움말 메뉴를 만들 수 있습니다. 각
카테고리(또는 Cog)에 대한 버튼을 만들고, 눌렀을 때 해당 카테고리의 명령을
보여주는 방식입니다. 행당 5개 버튼 제한에 유의해야 합니다【716329102970593†L5969-L6031】.

```python
class HelpMenu(discord.ui.View):
    def __init__(self, bot: commands.Bot):
        super().__init__(timeout=120)
        self.bot = bot
        # Cog 목록으로 버튼 생성
        for cog_name, cog in bot.cogs.items():
            button = discord.ui.Button(label=cog_name, style=discord.ButtonStyle.primary)
            button.callback = self.make_cog_callback(cog)
            self.add_item(button)

    def make_cog_callback(self, cog):
        async def callback(interaction: discord.Interaction):
            cmds = await self.bot.get_cog(cog.qualified_name).get_commands()
            embed = discord.Embed(title=f"{cog.qualified_name} 명령", description="")
            for cmd in cmds:
                embed.add_field(name=cmd.name, value=cmd.help or "설명 없음", inline=False)
            await interaction.response.send_message(embed=embed, ephemerial=True)
        return callback

@bot.command(name="helpme")
async def helpme(ctx):
    view = HelpMenu(ctx.bot)
    await ctx.send("도움말 카테고리를 선택하세요", view=view)
```

위 예제는 Cog 이름을 버튼으로 표시하고, 버튼을 누르면 해당 Cog에 포함된 명령을
임베드로 보여줍니다. 이러한 메뉴 방식은 명령이 많을 때 유용하며, 버튼
스타일과 행 구성을 조절하여 보기 좋게 만들 수 있습니다.

## slash 커맨드 도움말

슬래시 명령에서는 Discord 클라이언트가 기본 도움말 UI를 제공하지만, 추가
안내가 필요할 때는 `/help` 슬래시 명령을 직접 등록할 수 있습니다. 이때
`discord.app_commands.CommandTree`를 사용하여 설명과 옵션을 등록하고,
사용자가 선택할 수 있는 카테고리를 `Choice`로 제한할 수 있습니다.

```python
@bot.tree.command(name="help")
@app_commands.describe(category="도움말을 볼 카테고리")
@app_commands.choices(category=[app_commands.Choice(name=cog, value=cog) for cog in bot.cogs.keys()])
async def slash_help(interaction: discord.Interaction, category: app_commands.Choice[str]):
    cog = bot.get_cog(category.value)
    embed = discord.Embed(title=f"{cog.qualified_name} 명령 목록")
    for cmd in cog.get_commands():
        embed.add_field(name=cmd.name, value=cmd.description or "설명 없음", inline=False)
    await interaction.response.send_message(embed=embed, ephemerial=True)
```

## 사용자 경험을 위한 팁

- 명령어 이름과 설명을 짧고 명확하게 작성합니다.
- 자주 사용하는 명령은 별도의 그룹이나 카테고리에 배치하여 쉽게 찾게 합니다.
- 슬래시 명령에는 `description`과 각 옵션에 `description`을 반드시 작성하여
  Discord 클라이언트에서 올바르게 표시되도록 합니다.
- 도움말 메시지의 길이가 길어질 경우 페이지네이션이나 검색 기능을 추가해
  탐색성을 높입니다.

---

맞춤형 도움말 시스템을 통해 사용자는 원하는 기능을 빠르게 찾아 사용할 수
있습니다. 마지막 장에서는 앞서 배운 모든 기술을 종합해 봇을 완성하는 방법을
살펴봅니다.