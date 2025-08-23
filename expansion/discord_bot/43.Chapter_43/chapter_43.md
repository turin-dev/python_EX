# 43장 – 고급 셀렉트 메뉴

이 장에서는 드롭다운 형태의 셀렉트 메뉴를 더욱 세밀하게 커스터마이즈하고, 다양한 종류의
선택 도구를 만드는 방법을 배웁니다. 셀렉트 메뉴는 하나 또는 여러 값을 선택할 수 있는
UI 컴포넌트로, 로ール·채널·유저 선택 등 여러 유형이 있습니다.

## Select 메뉴의 매개변수

기본적인 셀렉트 메뉴는 `discord.ui.Select` 클래스로 구현됩니다. 문서에서는 다음과 같은
매개변수를 지원한다고 설명합니다【716329102970593†L6232-L6297】:

* **custom_id** – 상호작용 시 전송되는 고유 ID. 명시하지 않으면 자동 생성되며 100자까지 사용 가능합니다.
* **placeholder** – 아무 것도 선택되지 않았을 때 표시되는 안내 문구. 150자까지 지정할 수 있습니다.
* **min_values** / **max_values** – 사용자가 선택해야 하는 최소/최대 항목 수를 지정합니다. 기본값은 1이며 0~25 범위 내에서 설정 가능합니다.
* **options** – 선택할 옵션들의 리스트입니다. 최대 25개까지 추가할 수 있고, `label`, `value`, `description`, `emoji`, `default` 속성을 가집니다.
* **disabled** – 메뉴를 비활성화할지 여부.
* **required** – 모달에서만 사용되는 옵션으로, 선택이 필수인지 지정합니다.
* **row** – 컴포넌트가 배치될 행 번호를 지정합니다. 0~4 사이의 정수 값이며, 지정하지 않으면 자동으로 채워집니다【716329102970593†L6232-L6297】.

또한 `discord.py` 2.4 이상에서는 특정 유형의 객체만 선택할 수 있는 특수 메뉴를 제공합니다:

* **RoleSelect** – 길드의 역할(Role)들을 선택합니다.
* **ChannelSelect** – 텍스트·음성·스레드 등 특정 채널 유형을 선택할 수 있습니다.
* **UserSelect** – 유저를 선택하는 메뉴입니다.
* **MentionableSelect** – 유저와 역할을 모두 선택할 수 있습니다.

이러한 특수 메뉴들은 공통적으로 `min_values`, `max_values`, `placeholder`, `row` 등의 매개변수를
가집니다. 예를 들어 여러 역할을 선택하려면 `max_values`를 3으로 설정하고, 최소 선택 개수를 1로 유지할 수 있습니다.

## 예제: 과일 선택 메뉴

아래 예제는 사용자가 여러 과일을 선택할 수 있는 셀렉트 메뉴를 구현합니다. 옵션에는 라벨과 값,
설명이 포함되며, `min_values=1`, `max_values=3`으로 설정해 최소 1개에서 최대 3개의 과일을 선택하도록
합니다.

```python
import discord
from discord.ext import commands


class FruitView(discord.ui.View):
    def __init__(self):
        super().__init__()
        options = [
            discord.SelectOption(label="사과", value="apple", description="상큼한 사과"),
            discord.SelectOption(label="바나나", value="banana", description="달콤한 바나나"),
            discord.SelectOption(label="체리", value="cherry", description="새콤한 체리"),
            discord.SelectOption(label="수박", value="watermelon", description="시원한 수박"),
            discord.SelectOption(label="포도", value="grape", description="맛있는 포도")
        ]
        select = discord.ui.Select(
            placeholder="좋아하는 과일을 선택하세요",
            min_values=1,
            max_values=3,
            options=options,
            custom_id="fruit_select"
        )
        select.callback = self.on_select
        self.add_item(select)

    async def on_select(self, interaction: discord.Interaction):
        chosen = ", ".join(interaction.data.get("values", []))
        await interaction.response.send_message(f"선택한 과일: {chosen}", ephemeral=True)


async def setup(bot: commands.Bot):
    @bot.command(name="과일")
    async def fruit_cmd(ctx: commands.Context):
        await ctx.send("과일을 선택하세요", view=FruitView())
```

이 예제에서는 `interaction.data.get("values", [])`를 사용해 사용자가 선택한 값 목록을 가져옵니다. 콜백은
명령 처리 함수가 아닌 셀렉트 메뉴에 직접 연결되어 있습니다.

## 예제: 채널 선택 메뉴

특수 셀렉트 클래스를 사용하면 사용자가 채널을 선택하도록 제한할 수 있습니다. 예를 들어 텍스트 채널만
선택하도록 하려면 `discord.ui.ChannelSelect`의 `channel_types` 인자에 `discord.ChannelType.text`를
전달합니다.

```python
class AnnouncementView(discord.ui.View):
    def __init__(self):
        super().__init__()
        select = discord.ui.ChannelSelect(
            channel_types=[discord.ChannelType.text],
            placeholder="공지 채널을 선택하세요",
            min_values=1,
            max_values=1,
            custom_id="channel_select"
        )
        select.callback = self.on_select
        self.add_item(select)

    async def on_select(self, interaction: discord.Interaction):
        channel_id = interaction.data["values"][0]
        channel = interaction.guild.get_channel(int(channel_id))
        await interaction.response.send_message(f"선택한 채널: {channel.mention}",
                                               allowed_mentions=discord.AllowedMentions.none(),
                                               ephemeral=True)


async def setup(bot: commands.Bot):
    @bot.command(name="공지채널")
    async def announce_cmd(ctx: commands.Context):
        await ctx.send("공지 채널을 선택하세요", view=AnnouncementView())
```

`ChannelSelect`, `RoleSelect`, `UserSelect`, `MentionableSelect` 등은 용도에 맞게 선택지를 자동으로 채워주기 때문에
옵션을 수동으로 추가할 필요가 없습니다. `min_values`와 `max_values`를 적절히 설정해 선택 갯수를 제어하고,
`placeholder`를 사용해 사용자에게 안내 메시지를 제공합니다.

## 동적 옵션 구성

경우에 따라 선택 옵션을 데이터베이스나 API에서 가져와서 동적으로 생성해야 할 수도 있습니다. 그럴 때는
`options` 리스트를 런타임에 채운 뒤 `discord.ui.Select`를 생성하거나, 콜백 내부에서 `message.edit`
를 호출해 새 뷰와 셀렉트를 전달하는 방식으로 구현할 수 있습니다. 단, Discord API 제한으로 옵션 수는
최대 25개입니다【716329102970593†L6232-L6297】.

## 요약

셀렉트 메뉴는 복수 선택, 플레이스홀더, 옵션 리스트, 행(row) 위치 등 다양한 속성을 조정할 수 있습니다. 문서에 따르면
`min_values`와 `max_values`는 0~25 사이이며 옵션은 최대 25개까지 지정할 수 있습니다【716329102970593†L6232-L6297】.
특수 셀렉트 클래스(`RoleSelect`, `ChannelSelect` 등)를 사용하면 로컬 데이터베이스를 사용하지 않고도 편리하게 역할이나
채널을 선택할 수 있습니다. 동적 옵션을 생성할 때는 API 호출 횟수와 선택 항목 제한을 염두에 두어야 합니다.