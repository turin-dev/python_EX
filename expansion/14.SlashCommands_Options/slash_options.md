# 슬래시 커맨드 옵션과 선택지

슬래시 커맨드는 인자(옵션)를 상세하게 정의할 수 있으며, 각 인자에 대해 설명, 기본값, 범위 제한, 고정된 선택지, 자동 완성 등을 지정할 수 있습니다. 잘 설계된 옵션은 사용자가 명령어를 쉽게 이해하고 실수 없이 사용할 수 있도록 도와줍니다.

## 1. 인자 설명과 기본값

`@app_commands.describe()` 데코레이터는 각 인자에 대한 설명을 추가합니다. 설명은 명령 UI에 표시되어 사용자가 입력할 값을 이해하는 데 도움을 줍니다. 기본값을 지정하면 해당 인자는 선택 사항이 되며, 입력하지 않은 경우 기본값이 사용됩니다:

```python
from discord import app_commands

@bot.tree.command(name='remind', description='리마인더 설정')
@app_commands.describe(text='알림 내용', minutes='몇 분 후 알림을 보낼지')
async def remind(interaction: discord.Interaction, text: str, minutes: app_commands.Range[int, 1, 120] = 10):
    await interaction.response.send_message(f'{minutes}분 후 알림: {text}')
```

여기서 `Range[int, 1, 120]`는 1에서 120 사이의 정수만 허용하는 옵션을 정의합니다. 기본값 `10`을 주었기 때문에 `/remind 내용`과 같이 호출하면 10분 후 알림을 전송합니다.

## 2. 선택지 제한

선택지를 지정하여 사용자가 미리 정의된 옵션 중에서만 선택하게 할 수 있습니다. `@app_commands.choices()` 데코레이터는 인자 이름과 선택 리스트를 매핑합니다. 선택지는 `app_commands.Choice` 객체나 `{'이름': 값}` 형태의 딕셔너리로 지정할 수 있습니다:

```python
@bot.tree.command(name='choose', description='과일을 선택')
@app_commands.choices(fruit=[
    app_commands.Choice(name='사과', value=1),
    app_commands.Choice(name='바나나', value=2),
    app_commands.Choice(name='포도', value=3)
])
async def choose(interaction: discord.Interaction, fruit: app_commands.Choice[int]):
    fruit_map = {1: '사과', 2: '바나나', 3: '포도'}
    await interaction.response.send_message(f'선택된 과일: {fruit_map[fruit.value]}')
```

선택지를 정의하면 클라이언트는 드롭다운 메뉴를 제공하고, 사용자는 해당 옵션 중 하나를 선택해야 합니다. 선택지 값은 정수, 문자열 등 다양한 타입을 사용할 수 있습니다.

## 3. 동적 선택지와 자동 완성

`discord.py`는 정적으로 선택지를 지정하는 것 외에도, 사용자의 입력에 따라 동적으로 옵션을 제안하는 **자동 완성(autocomplete)** 기능을 제공합니다. 매개변수에 `Autocomplete[str]`과 같이 타입을 지정하고, 명령에 `@app_commands.autocomplete()` 데코레이터로 콜백 함수를 연결하면 사용자 입력을 기반으로 옵션을 제안할 수 있습니다:

```python
from discord import app_commands

async def search_games(interaction: discord.Interaction, current: str) -> list[app_commands.Choice[str]]:
    # 데이터베이스나 API에서 검색
    games = ['스타크래프트', '리그오브레전드', '오버워치']
    return [app_commands.Choice(name=g, value=g) for g in games if current.lower() in g.lower()]

@bot.tree.command(name='play', description='게임을 선택')
@app_commands.autocomplete(game=search_games)
async def play(interaction: discord.Interaction, game: str):
    await interaction.response.send_message(f'{game}을(를) 시작합니다!')
```

사용자가 입력창에 단어를 타이핑하면 `search_games` 콜백이 실행되어 일치하는 게임 목록을 반환합니다. 자동 완성은 최대 25개의 항목을 반환할 수 있습니다.

## 4. 채널 유형과 기타 타입

슬래시 커맨드는 Discord 객체를 매개변수 타입으로 사용할 수 있습니다. 예를 들어 특정 텍스트 채널을 선택하도록 제한하려면 `channel_types` 옵션을 사용합니다:

```python
@bot.tree.command(name='announce', description='채널에 공지 전송')
async def announce(interaction: discord.Interaction, channel: discord.TextChannel, *, message: str):
    await channel.send(message)
    await interaction.response.send_message('전송 완료', ephemeral=True)
```

채널 매개변수에는 `channel_types` 키워드 인자를 지정해 `TextChannel`, `VoiceChannel`, `CategoryChannel` 등의 유형을 제한할 수 있습니다:

```python
@bot.tree.command(name='move', description='사용자를 음성 채널로 이동')
async def move(interaction: discord.Interaction, member: discord.Member, *, voice_channel: discord.VoiceChannel):
    await member.move_to(voice_channel)
    await interaction.response.send_message('이동 완료')
```

## 5. 옵션 순서와 필수성

슬래시 커맨드의 인자 순서는 함수 정의 순서에 따라 결정되며, 필수 인자는 항상 선택적 인자 앞에 와야 합니다. 기본값이 없는 인자는 필수이며, Discord 클라이언트는 이를 미리 알려줍니다. 인자 이름은 32자 이하, 설명은 100자 이하로 제한됩니다.

옵션과 선택지를 적절히 사용하면 사용자가 명령을 쉽게 입력하고 실수를 줄일 수 있습니다. 다음 장에서는 컨텍스트 메뉴와 다른 상호작용 유형을 사용하여 명령의 범위를 넓혀 봅니다.



