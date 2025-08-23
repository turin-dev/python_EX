# 44장 – 슬래시 명령 그룹과 하위 명령

복잡한 기능을 제공하는 봇에서는 명령을 의미별로 **그룹**으로 묶어야 관리가 쉬워집니다. Discord의 애플리케이션 명령 API는 `Group` 클래스를 제공하여 슬래시 명령을 계층 구조로 구성할 수 있게 합니다. 하위 명령은 `/그룹 명령` 형태로 호출되며, 그룹 내에서는 공통 권한과 설명을 재사용할 수 있습니다.

## AppCommandGroup 소개

`discord.app_commands.AppCommandGroup` 는 애플리케이션 명령 그룹을 구현하는 클래스입니다. 문서에서는 주로 상속을 통해 그룹을 만든다고 설명합니다【716329102970593†L10228-L10267】. 그룹 정의 시에는 다음과 같은 매개변수를 사용할 수 있습니다:

* **name** – 그룹 이름. 지정하지 않으면 클래스 이름을 케밥 케이스로 변환한 값이 사용됩니다【716329102970593†L10248-L10250】.
* **description** – 그룹 설명. 지정하지 않으면 클래스의 첫 줄 docstring이 사용됩니다【716329102970593†L10252-L10254】.
* **default_permissions** – 이 그룹을 실행할 수 있는 기본 권한을 지정합니다. 이 값은 서버 관리자가 덮어쓸 수 있으며, 빈 권한 집합을 지정하면 길드 관리자만 사용 가능합니다【716329102970593†L10262-L10267】.
* **guild_only** – `True`로 설정하면 DM에서는 명령을 사용할 수 없으며 길드 내에서만 동작합니다【716329102970593†L10271-L10275】. 단, 서브커맨드에는 적용되지 않습니다.
* **nsfw** – NSFW 채널에서만 사용하도록 제한할지 여부입니다【716329102970593†L10277-L10280】.

그룹 클래스는 명령어를 서브메서드로 정의하거나, 데코레이터를 사용해 동적으로 추가할 수 있습니다. 그룹을 재사용하기 위해서는 `bot.tree.add_command(MyGroup())`나 `bot.tree.add_command(group_instance, guild=guild)`로 등록하고 `bot.tree.sync()`를 호출해 동기화해야 합니다.

## 예제: 신고 기능 그룹 만들기

다음 예제에서는 `/신고` 명령 그룹을 만들고 하위 명령으로 `bug`와 `feature`를 정의합니다. 사용자는 버그 신고와 기능 요청을 구분하여 입력할 수 있고, 각 명령은 별도의 설명을 가집니다.

```python
import discord
from discord.ext import commands


class ReportGroup(discord.app_commands.Group):
    def __init__(self):
        super().__init__(
            name="신고",
            description="버그 또는 기능 요청을 접수합니다",
            guild_only=True
        )

    @discord.app_commands.command(name="버그", description="버그를 신고합니다")
    async def bug(self, interaction: discord.Interaction, title: str, description: str):
        # 여기서는 데이터베이스나 이슈 트래킹 시스템에 기록할 수 있습니다.
        await interaction.response.send_message(
            f"버그 '{title}'가 접수되었습니다!", 
            allowed_mentions=discord.AllowedMentions.none(),
            ephemeral=True
        )

    @discord.app_commands.command(name="기능", description="새로운 기능을 제안합니다")
    async def feature(self, interaction: discord.Interaction, title: str, description: str):
        await interaction.response.send_message(
            f"기능 요청 '{title}'가 접수되었습니다!", 
            allowed_mentions=discord.AllowedMentions.none(),
            ephemeral=True
        )


async def setup(bot: commands.Bot):
    # 그룹을 트리(register)에 추가합니다. 전역(Global) 명령으로 등록될 수 있습니다.
    group = ReportGroup()
    bot.tree.add_command(group)

    # 봇 준비 시 전역 명령을 동기화합니다. 빠른 테스트를 위해 특정 길드에만 동기화할 수도 있습니다.
    @bot.event
    async def on_ready():
        await bot.tree.sync()  # 또는 await bot.tree.sync(guild=guild)로 특정 길드에만 배포
        print("신고 명령 그룹이 동기화되었습니다.")
```

이 예제에서 `ReportGroup`은 `app_commands.Group`를 상속하고 두 개의 명령을 정의합니다. 명령은 그룹 내부 메서드로 정의될 때 자동으로 `/신고 버그`, `/신고 기능` 형태로 등록됩니다. 그룹을 트리에 등록한 후 `bot.tree.sync()`를 호출하여 Discord 서버와 동기화해야 실제로 사용할 수 있습니다.

## 하위 명령과 서브그룹 추가하기

그룹 안에 또 다른 그룹을 중첩할 수 있습니다. 예를 들어 `/관리` 그룹 아래에 `/공지`와 `/공지 삭제` 같은 명령을 배치하거나, `/음악` 그룹 아래에 `/재생`, `/정지`, `/목록` 서브그룹을 만들 수 있습니다. 이를 위해 `app_commands.Group`를 상속한 클래스를 하위 그룹으로 추가하거나, `@parent_group.command()` 데코레이터를 사용할 수 있습니다. 주의할 점은 Discord API 제한으로 서브그룹 깊이는 최대 1단계까지 지원된다는 것입니다.

## 기본 권한과 제약

그룹과 하위 명령은 `default_permissions`를 통해 기본 실행 권한을 지정할 수 있습니다. 이는 길드 관리자가 클라이언트에서 오버라이드할 수 있으며, 설정하지 않으면 누구나 명령을 사용할 수 있습니다. 또한 `guild_only=True`를 지정하면 DM에서는 명령이 숨겨집니다【716329102970593†L10271-L10275】. NSFW 플래그를 사용하면 NSFW 채널에서만 명령을 실행할 수 있지만, 서브커맨드에는 적용되지 않는 제한이 있습니다【716329102970593†L10271-L10280】.

## 요약

슬래시 명령 그룹을 통해 명령을 계층 구조로 구성하면 사용성과 관리성이 향상됩니다. `AppCommandGroup`를 상속하여 그룹 이름, 설명, 기본 권한을 지정할 수 있으며, `bot.tree.add_command()`와 `bot.tree.sync()`로 Discord 서버에 등록합니다. 하위 명령을 정의하면 `/그룹 명령` 형태로 호출할 수 있고, 서브그룹을 사용하면 더 복잡한 명령 체계를 구성할 수 있습니다【716329102970593†L10228-L10275】.