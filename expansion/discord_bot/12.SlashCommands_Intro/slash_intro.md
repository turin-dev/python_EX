# 슬래시 커맨드 소개

`discord.py` 2.x에서는 기존 접두사 기반 명령어 시스템 외에 **슬래시 커맨드(slash command)** 를 지원합니다. 슬래시 커맨드는 Discord 클라이언트의 채팅 입력창에 `/`를 입력하면 표시되는 내장 UI로, 사용자가 봇 명령을 쉽게 검색하고 인자를 자동 완성할 수 있게 해 줍니다. 이러한 명령은 Discord 서버에 사전에 등록되어야 하며, 등록 후에는 Discord가 명령을 호출할 때 `discord.Interaction` 객체를 전달합니다【716329102970593†L162-L164】.

## 1. CommandTree와 기본 구조

슬래시 커맨드는 `discord.app_commands.CommandTree` 인스턴스를 통해 관리됩니다. `commands.Bot`은 `tree` 속성으로 기본 CommandTree를 제공하므로, 별도의 인스턴스를 생성하지 않고 `bot.tree`를 사용할 수 있습니다. 슬래시 커맨드를 등록하려면 `@bot.tree.command()` 데코레이터를 사용합니다. 첫 번째 인자는 `Interaction` 객체이며, 이는 기존 명령어의 `Context`와 유사하지만 응답 방식이 다릅니다. 아래는 간단한 예제입니다:

```python
from discord.ext import commands
from discord import app_commands

bot = commands.Bot(command_prefix='!', intents=discord.Intents.default())

@bot.event
async def on_ready():
    # 명령어를 Discord 서버에 동기화
    await bot.tree.sync()
    print('슬래시 커맨드 동기화 완료')

@bot.tree.command(name='hello', description='인사 메시지를 보냅니다')
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message(f'{interaction.user.mention}님, 안녕하세요!')

bot.run('YOUR_TOKEN')
```

위 예제에서 `@bot.tree.command()` 데코레이터는 슬래시 명령을 정의하며, `name`과 `description`은 Discord 클라이언트에 표시되는 명령 이름과 설명입니다. `bot.tree.sync()`를 호출하면 봇이 슬래시 명령을 Discord API에 등록하고 동기화합니다. 이는 봇이 준비된 후 한 번만 호출하면 됩니다.

## 2. 글로벌 vs 길드 명령

슬래시 커맨드는 **글로벌**(모든 길드에서 사용 가능한)로 등록할 수 있고, 특정 길드에만 등록할 수도 있습니다. 글로벌 명령은 등록 후 최대 한 시간 정도까지 전파 지연이 있을 수 있지만, 길드 전용 명령은 즉시 업데이트됩니다. 길드 전용 명령은 개발 과정에서 빠른 테스트에 유리합니다.

```python
@bot.tree.command(name='guild-hello', description='길드 전용 인사', guild=discord.Object(id=GUILD_ID))
async def guild_hello(interaction: discord.Interaction):
    await interaction.response.send_message('이 명령은 특정 길드에서만 사용 가능합니다.')
```

또는 명령어를 등록한 후 `await bot.tree.sync(guild=discord.Object(id=GUILD_ID))`를 호출하면 해당 길드에만 명령이 동기화됩니다.

## 3. 설명과 로컬라이제이션

Discord는 슬래시 커맨드의 이름과 설명을 현지화할 수 있는 기능을 제공하고 있습니다. `app_commands.locale_str`를 사용하면 여러 언어에 대한 번역을 정의할 수 있으며, `choices`와 `autocomplete`를 통해 인자에 대한 옵션과 자동 완성 기능을 구현할 수 있습니다. 사용자 경험을 향상시키기 위해 명령어 이름은 짧고 명확하게, 설명은 구체적으로 작성하는 것이 좋습니다.

## 4. 동기화 타이밍과 개발 팁

- 슬래시 커맨드를 추가하거나 수정한 경우, `bot.tree.sync()`를 호출해야 변경 사항이 Discord 서버에 적용됩니다. 전역 명령은 퍼지 시간이 길므로 개발 중에는 길드 전용으로 등록하여 빠르게 테스트하는 것이 좋습니다.
- 명령 이름은 서버 전체에서 고유해야 하며, 대소문자를 구분하지 않습니다. 동일한 이름을 가진 명령을 두 번 등록하면 오류가 발생합니다.
- 슬래시 커맨드는 메시지 삭제나 수정 등 상태 변화 없이 대화형 응답을 제공하며, `defer()`를 통해 지연 응답을 할 수 있습니다. 모달이나 버튼과 같은 컴포넌트는 `Interaction` 객체를 통해 처리합니다.

이번 장에서는 슬래시 커맨드의 기본 개념과 등록 방법을 살펴보았습니다. 다음 장에서는 슬래시 커맨드 옵션과 서브커맨드를 정의하고, 상호작용을 더욱 풍부하게 만드는 방법을 배웁니다.



