# 슬래시 커맨드 등록과 동기화

슬래시 커맨드를 작성한 후에는 Discord API에 명령을 **등록(sync)** 해야 합니다. 등록하지 않은 명령은 클라이언트에서 인식할 수 없으므로, 봇이 시작될 때 한 번만 동기화하는 것이 일반적입니다. 이 장에서는 명령 등록과 동기화의 다양한 옵션을 살펴보고, 글로벌과 길드 전용 명령을 효율적으로 관리하는 방법을 설명합니다.

## 1. 동기화 기본

`Bot.tree.sync()` 메서드는 봇의 `CommandTree`에 정의된 모든 명령을 Discord 서버에 등록합니다. 봇이 처음 시작하거나 명령을 추가/수정한 경우, `on_ready` 이벤트에서 다음과 같이 호출하는 것이 일반적입니다:

```python
@bot.event
async def on_ready():
    # 글로벌 명령과 길드 명령을 모두 동기화
    await bot.tree.sync()
    print('모든 슬래시 커맨드가 동기화되었습니다.')
```

이 호출은 각 명령에 대해 Discord API에 HTTP 요청을 보내며, 전체 명령 목록을 서버에 저장합니다. 글로벌 명령은 전파에 시간이 걸릴 수 있기 때문에, 개발 시에는 길드 전용 명령으로 먼저 테스트하는 것이 좋습니다.

## 2. 개별 길드에만 동기화

개발이나 테스트 단계에서는 특정 길드에만 명령을 등록하면 빠른 피드백을 얻을 수 있습니다. `sync(guild=discord.Object(id=...))`를 호출하면 해당 길드의 명령만 업데이트합니다. 또한 `copy_global_to(guild=...)`를 사용하면 이미 정의된 글로벌 명령을 지정한 길드로 복사할 수 있습니다:

```python
TEST_GUILD = discord.Object(id=1234567890)

@bot.event
async def on_ready():
    # 글로벌 명령을 테스트 길드에 복사
    bot.tree.copy_global_to(guild=TEST_GUILD)
    await bot.tree.sync(guild=TEST_GUILD)
    print('테스트 길드에 명령을 동기화했습니다.')
```

길드 전용 동기화는 거의 즉시 반영되므로, 명령을 수정할 때마다 빠르게 테스트할 수 있습니다. 테스트가 끝나면 `sync()`를 호출하여 글로벌로 배포합니다.

## 3. 명령 추가와 삭제

슬래시 커맨드는 데코레이터를 통해 정의하는 것 외에도, 런타임에 `bot.tree.add_command()`를 호출하여 동적으로 추가할 수 있습니다. 삭제하려면 `bot.tree.remove_command('name', type=discord.AppCommandType.chat_input)`를 사용합니다. 명령을 삭제한 후에는 다시 `sync()`를 호출해야 변경 사항이 반영됩니다.

## 4. 명령 이름과 설명 길이 제한

Discord는 슬래시 커맨드 이름과 설명에 길이 제한을 두고 있습니다. 이름은 1~32자의 소문자와 하이픈(-)만 사용해야 하며, 설명은 1~100자 사이여야 합니다. 이러한 제한을 초과하면 등록 시 `HTTPException`이 발생합니다. 따라서 명령어의 목적을 간결하고 명확하게 표현하도록 주의해야 합니다.

## 5. 권한과 기본 멤버 권한 설정

슬래시 커맨드는 기본적으로 모든 사용자에게 공개되지만, `default_member_permissions` 매개변수를 사용하여 명령 실행 권한을 제한할 수 있습니다. 예를 들어, 메시지를 관리할 수 있는 권한을 가진 사용자만 명령을 사용할 수 있도록 설정할 수 있습니다:

```python
@bot.tree.command(name='purge', description='메시지 삭제', default_member_permissions=discord.Permissions(manage_messages=True))
async def purge(interaction: discord.Interaction, amount: int):
    await interaction.channel.purge(limit=amount)
    await interaction.response.send_message(f'{amount}개의 메시지를 삭제했습니다.', ephemeral=True)
```

`ephemeral=True` 옵션은 응답 메시지를 명령 호출자에게만 표시합니다. 권한 설정을 올바르게 사용하면 서버 관리 기능이 담긴 명령을 안전하게 배포할 수 있습니다.

슬래시 커맨드의 동기화와 권한 관리 방법을 이해하고 나면, 복잡한 옵션과 서브커맨드를 추가하는 데 필요한 기초가 마련됩니다. 다음 장에서는 명령 옵션과 하위 명령을 정의하는 법을 다룰 것입니다.



