# 설문과 투표 시스템 구현

커뮤니티 운영에서 **설문 조사**와 **투표**는 사용자 의견을 수렴하고 의사결정을
돕는 중요한 도구입니다. 디스코드에서는 리액션, 버튼, 셀렉트 메뉴 등 다양한
UI 컴포넌트를 활용해 상호작용형 설문을 손쉽게 구현할 수 있습니다. 이 장에서는
간단한 예/아니오 투표부터 여러 옵션을 가진 설문까지 여러 방식으로 구현하는
방법을 자세히 소개합니다.

## 방법 1: 리액션을 이용한 기본 투표

리액션(이모지)을 이용한 투표는 모든 멤버가 이해하기 쉽고, 오버헤드가 거의
없습니다. 봇은 특정 메시지에 👍/👎 이모지를 추가하고, `on_raw_reaction_add`
이벤트에서 투표 결과를 집계합니다. 단점은 옵션 수가 이모지 수에 한정되고,
중복 투표를 방지하려면 추가 로직이 필요합니다.

```python
class ReactionPoll(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.votes = {}  # message_id -> {user_id: emoji}

    @commands.command()
    async def poll(self, ctx, *, question: str):
        msg = await ctx.send(f"{question}\n👍 = 찬성, 👎 = 반대")
        await msg.add_reaction("👍")
        await msg.add_reaction("👎")
        self.votes[msg.id] = {}

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.message_id not in self.votes:
            return
        # 중복 투표 방지: 이전 표 삭제
        user_votes = self.votes[payload.message_id]
        for user_id, emoji in list(user_votes.items()):
            if user_id == payload.user_id and emoji != str(payload.emoji):
                channel = self.bot.get_channel(payload.channel_id)
                message = await channel.fetch_message(payload.message_id)
                await message.remove_reaction(emoji, payload.member)
        self.votes[payload.message_id][payload.user_id] = str(payload.emoji)
```

이 방식은 단순하지만 투표 옵션을 추가하는 것이 번거롭고 메시지에 많은
이모지를 추가해야 합니다. 따라서 버튼과 셀렉트 메뉴를 사용한 방식이 더 편리합니다.

## 방법 2: 버튼을 이용한 선택형 투표

버튼은 참여자가 클릭만 하면 되므로 투표 과정을 간소화합니다. `discord.ui.Button`
의 `label`에 옵션을 지정하고, 버튼이 눌릴 때 콜백에서 집계합니다. 버튼은 라벨,
스타일, 커스텀 ID 등을 정의할 수 있으며, 동일한 행(row)에 최대 5개를 배치할
수 있습니다【716329102970593†L5969-L6031】. 투표를 마치면 버튼을 비활성화해서
추가 투표를 방지할 수 있습니다.

```python
from discord.ui import View, button

class ButtonPoll(View):
    def __init__(self, options: list[str], timeout: int = 60):
        super().__init__(timeout=timeout)
        self.options = options
        self.results: dict[str, set[int]] = {opt: set() for opt in options}

    async def disable_all(self, interaction):
        for child in self.children:
            child.disabled = True
        await interaction.response.edit_message(view=self)

    @button(label="종료", style=discord.ButtonStyle.danger, row=1)
    async def end(self, _button, interaction):
        await self.disable_all(interaction)
        summary = "\n".join(f"{opt}: {len(voters)}표" for opt, voters in self.results.items())
        await interaction.followup.send(f"투표 종료! 결과:\n{summary}")

    async def on_timeout(self) -> None:
        # 시간 초과 시 자동 종료
        message = self.message  # View가 바인딩될 때 자동 설정
        channel = message.channel
        # fallback: 수동으로 메시지 가져오기 가능
        summary = "\n".join(f"{opt}: {len(voters)}표" for opt, voters in self.results.items())
        await channel.send(f"투표 시간 초과! 결과:\n{summary}")

    # 버튼 동적 생성
    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        # 각 옵션에 대한 버튼 처리
        return True

```

버튼을 동적으로 생성하려면 `View.__init__`에서 반복문으로 `discord.ui.Button` 인스턴스를 만들고
`self.add_item()`으로 추가합니다. 버튼의 `custom_id`를 지정하면 영구 뷰로도 사용할 수 있습니다. 자세한 사용법은
"버튼 고급" 장을 참고하세요【716329102970593†L4889-L4924】.

## 방법 3: 셀렉트 메뉴를 이용한 설문

옵션이 많거나 다중 선택이 필요한 설문에는 셀렉트 메뉴가 효과적입니다. `discord.ui.Select`
의 `options` 목록에 최대 25개의 항목을 지정할 수 있고, `min_values`/`max_values`
를 통해 선택 가능 개수를 제어할 수 있습니다. 사용자가 선택을 완료하면 `callback`
에서 `values` 속성을 통해 선택한 값을 얻습니다.

```python
from discord.ui import View, Select

class SurveyView(View):
    def __init__(self):
        super().__init__(timeout=120)
        options = [discord.SelectOption(label=f"옵션 {i}", value=str(i)) for i in range(1, 6)]
        select = Select(placeholder="선택하세요", options=options, min_values=1, max_values=3)

        async def callback(interaction: discord.Interaction):
            chosen = ", ".join(select.values)
            await interaction.response.send_message(f"선택하신 옵션: {chosen}", ephemeral=True)
            self.stop()
        select.callback = callback
        self.add_item(select)

@bot.command()
async def survey(ctx):
    view = SurveyView()
    await ctx.send("설문 조사에 참여하세요", view=view)
```

## 결과 집계와 동시성

투표 시스템을 설계할 때는 중복 투표를 방지하고, 투표 중에 결과가 실시간으로 업데이트되도록 동시성을 관리해야 합니다. 예를 들어 버튼 투표에서는 각 버튼 클릭 콜백에서 `interaction.user.id`를 사용해 사용자 ID를 저장한 뒤, 다시 누르면 취소하거나 변경하게 만들 수 있습니다. `asyncio.Lock`을 사용해 여러 사용자가 동시에 클릭할 때 데이터 경쟁을 방지할 수 있습니다.

또한 시간 제한을 두고 `View`의 `timeout`이나 `asyncio.wait_for`를 이용해 설문을 종료하는 것이 좋습니다. 설문 종료 후에는 버튼과 셀렉트를 비활성화해 투표를 더 이상 받지 않도록 해야 합니다.

---

이 장을 통해 다양한 방식의 설문과 투표를 구현하는 법을 익혔습니다. 다음 장에서는 UI 컴포넌트를 더 세밀하게 조정하고 동적으로 변경하는 방법을 살펴봅니다.