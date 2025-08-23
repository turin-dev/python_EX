# 40장 – 슬래시 명령 자동완성과 선택지

대화형 경험을 개선하기 위해 슬래시 명령에는 자동완성 기능을 제공할 수 있습니다. 사용자가 입력을 시작하면 봇이 가능한 옵션을 제안하며, `discord.app_commands`의 `@app_commands.autocomplete()` 데코레이터를 사용해 동적으로 옵션 목록을 제공합니다. 또한 제한된 선택지를 명시적으로 정의하려면 `app_commands.Choice`를 사용할 수 있습니다.

## 고정 선택지

미리 정의된 값 집합을 옵션으로 제공하려면 `choices` 매개변수에 `app_commands.Choice` 객체 리스트를 전달합니다. 예를 들어 색상을 선택하는 명령은 다음과 같습니다.

```python
@bot.tree.command(name="color", description="색상을 선택합니다")
@app_commands.choices(
    colour=[
        app_commands.Choice(name="빨강", value=1),
        app_commands.Choice(name="초록", value=2),
        app_commands.Choice(name="파랑", value=3),
    ]
)
async def color(interaction: discord.Interaction, colour: app_commands.Choice[int]):
    await interaction.response.send_message(f"선택한 색상: {colour.name}")
```

사용자는 `/color` 명령을 입력할 때 드롭다운으로 세 가지 색상 중 하나를 선택할 수 있습니다.

## 동적 자동완성

자동완성 함수는 사용자가 입력한 부분 문자열(`current`)을 받아 관련 항목을 반환해야 합니다. 반환 값은 `app_commands.Choice` 목록으로, 최대 25개 항목까지 제공할 수 있습니다. 아래 예제는 사용자가 서버 내의 멤버를 이름으로 검색해 선택할 수 있도록 합니다.

```python
@app_commands.command(name="dm", description="사용자에게 DM을 보냅니다")
@app_commands.autocomplete(member=lambda interaction, current: [
    app_commands.Choice(name=member.display_name, value=member.id)
    for member in interaction.guild.members
    if current.lower() in member.display_name.lower()
][:25])
async def dm(interaction: discord.Interaction, member: discord.Member, *, message: str):
    await member.send(message)
    await interaction.response.send_message("DM을 전송했습니다", ephemeral=True)
```

사용자가 `/dm` 명령을 입력하면서 멤버 이름을 몇 글자라도 입력하면, 봇이 해당 문자열을 포함하는 멤버를 최대 25명까지 자동완성 목록으로 제시합니다. 자동완성 함수는 반드시 `interaction`과 `current` 두 인자를 받아야 합니다.

## 사용자 정의 객체 반환

반환 값으로 문자열이나 숫자 대신 Discord 객체를 사용할 수도 있습니다. 예를 들어 채널 자동완성을 구현하려면 `discord.TextChannel`을 타입으로 선언하고, 자동완성 함수에서 채널 객체 목록을 반환하면 됩니다. 이 경우 선택된 채널 객체가 명령 인자로 그대로 전달됩니다.

## 요약

자동완성과 선택지는 슬래시 명령의 사용자 경험을 크게 향상시킵니다. `app_commands.Choice`로 고정된 목록을 제공하고, `@app_commands.autocomplete`로 동적으로 목록을 생성할 수 있습니다. 각 자동완성 함수는 입력 문자열을 기반으로 최대 25개의 제안을 반환해야 하며, 이는 서버 규모와 사용 사례에 따라 적절히 필터링해야 합니다【230406618874054†L25-L36】.

