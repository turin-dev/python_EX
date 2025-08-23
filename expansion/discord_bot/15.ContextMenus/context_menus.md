# 컨텍스트 메뉴

**컨텍스트 메뉴(Context Menu)**는 Discord 클라이언트에서 사용자나 메시지를 우클릭하거나 옵션 메뉴를 열었을 때 표시되는 명령입니다. 슬래시 커맨드와 달리 별도의 명령어 입력 없이 대상 객체를 지정할 수 있어 특정 항목에 대해 빠른 동작을 수행할 때 유용합니다. 컨텍스트 메뉴는 크게 두 종류가 있습니다:

1. **유저 컨텍스트 메뉴**: 길드 멤버나 DM 유저를 대상으로 실행됩니다. 예: 프로필 보기, DM 보내기 등.
2. **메시지 컨텍스트 메뉴**: 특정 메시지를 대상으로 실행됩니다. 예: 메시지 내용 분석, 인용 등.

컨텍스트 메뉴를 정의하려면 `@bot.tree.context_menu(name=..., guild=...)` 데코레이터를 사용합니다. 첫 번째 매개변수는 `Interaction`이고, 두 번째 매개변수는 대상 객체(`discord.Member` 또는 `discord.Message`)입니다. 다음은 각각의 예제입니다:

```python
from discord import app_commands

@bot.tree.context_menu(name='유저 정보 보기')
async def show_user_info(interaction: discord.Interaction, member: discord.Member):
    # 유저 프로필 정보 출력
    embed = discord.Embed(title='유저 정보', description=f'{member.mention}', colour=discord.Colour.blue())
    embed.add_field(name='ID', value=member.id)
    embed.set_thumbnail(url=member.display_avatar.url)
    await interaction.response.send_message(embed=embed, ephemeral=True)

@bot.tree.context_menu(name='메시지 길이 세기')
async def count_message_chars(interaction: discord.Interaction, message: discord.Message):
    length = len(message.content)
    await interaction.response.send_message(f'이 메시지는 {length}자의 길이를 가지고 있습니다.', ephemeral=True)
```

위 예제에서 `show_user_info`는 유저 컨텍스트 메뉴로 등록되고, 우클릭 메뉴에서 **유저 정보 보기** 옵션을 선택하면 해당 유저의 정보를 DM 또는 서버 채널에 표시합니다. `count_message_chars`는 메시지 컨텍스트 메뉴로 등록되어, 선택한 메시지의 길이를 계산하여 응답합니다. 응답을 호출한 사용자에게만 보이도록 하려면 `ephemeral=True`를 지정할 수 있습니다.

## 등록과 동기화

컨텍스트 메뉴도 슬래시 커맨드와 마찬가지로 Discord API에 등록해야 합니다. `bot.tree.sync()`를 호출하면 컨텍스트 메뉴가 서버에 동기화됩니다. 길드 전용으로 등록하려면 `guild=discord.Object(id=...)` 매개변수를 `context_menu` 데코레이터에 전달하거나, `sync(guild=...)`를 사용하여 동기화할 수 있습니다. 컨텍스트 메뉴 이름은 슬래시 커맨드와 동일한 제약을 받으며(1~32자), 다른 명령과 중복되면 안 됩니다.

컨텍스트 메뉴는 타겟 객체에 따라 적절한 파라미터 타입(`discord.Member` 혹은 `discord.Message`)을 지정해야 합니다. 잘못된 타입을 사용하면 `TypeError`가 발생합니다. 컨텍스트 메뉴와 슬래시 커맨드의 차이를 이해하고 적절히 사용하면, 사용자 인터페이스를 더욱 직관적으로 만들 수 있습니다.



