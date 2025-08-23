# 동적 컴포넌트와 UI 고급 기법

디스코드의 UI 컴포넌트는 버튼과 셀렉트 메뉴뿐 아니라 **모달** 등 다양한 요소가
있습니다. 이 장에서는 사용자 입력이나 외부 데이터에 따라 동적으로 변하는 옵션을
제공하는 기술과, 여러 컴포넌트를 조합한 멀티 스텝 인터페이스를 구현하는
방법을 다룹니다. 또한 뷰의 생명주기와 권한 검사를 활용해 보안을 강화하는
방법도 소개합니다.

## 동적 셀렉트 메뉴 생성

정적인 `Select`는 옵션을 미리 정의해야 하지만, 사용자의 역할, 외부 API 결과
등에 따라 옵션을 생성해야 할 때가 있습니다. `discord.ui.Select`는 콜백에서
새로운 뷰를 보내거나, `@app_commands.autocomplete`를 사용해 슬래시
커맨드에서 동적 자동완성을 제공할 수 있습니다. 메시지 기반에서는 다음과 같이
API 호출 후 옵션을 생성할 수 있습니다:

```python
from discord.ui import View, Select
import aiohttp

class GitHubRepoSelect(View):
    def __init__(self, user: str):
        super().__init__(timeout=60)
        self.user = user
        self.select = Select(placeholder="저장소를 선택하세요", options=[])
        self.select.callback = self._selected
        self.add_item(self.select)
        # 동적 옵션 로딩 태스크 시작
        self.task = asyncio.create_task(self.load_options())

    async def load_options(self):
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://api.github.com/users/{self.user}/repos") as resp:
                data = await resp.json()
        self.select.options = [discord.SelectOption(label=repo["name"], value=repo["name"]) for repo in data[:25]]
        # 옵션을 갱신하기 위해 메시지 편집
        await self.message.edit(view=self)

    async def _selected(self, interaction: discord.Interaction):
        await interaction.response.send_message(f"선택한 저장소: {self.select.values[0]}", ephemeral=True)
        self.stop()

@bot.command()
async def choose_repo(ctx, user: str):
    view = GitHubRepoSelect(user)
    view.message = await ctx.send(f"{user}의 저장소를 조회 중...", view=view)
```

이 예제에서 `load_options()` 메서드는 GitHub API를 호출하여 옵션 목록을 동적으로
채웁니다. 옵션이 업데이트되면 메시지를 편집하여 새 옵션이 반영된 셀렉트 메뉴를
보여줍니다.

## 모달을 이용한 다단계 입력

`discord.ui.Modal`은 사용자가 여러 필드를 작성할 수 있는 팝업 창입니다. 모달을
중첩해 단계별 설문을 만들 수 있으며, 슬래시 명령이나 버튼 콜백에서 호출할 수
있습니다. 예를 들어 사용자의 피드백을 수집하는 두 단계 설문을 만들어 봅시다.

```python
from discord.ui import Modal, TextInput

class FeedbackStepOne(Modal, title="1단계: 기본 정보"):
    name = TextInput(label="이름", placeholder="닉네임을 적어주세요", max_length=32)
    age = TextInput(label="나이", placeholder="숫자로 입력", max_length=3)

    async def on_submit(self, interaction: discord.Interaction):
        # 다음 단계 모달 호출
        step_two = FeedbackStepTwo(self.name.value, self.age.value)
        await interaction.response.send_modal(step_two)

class FeedbackStepTwo(Modal):
    def __init__(self, name: str, age: str):
        super().__init__(title="2단계: 의견 작성")
        self.name = name
        self.age = age
        self.comment = TextInput(label="의견", style=discord.TextStyle.long, max_length=500)

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.send_message(
            f"감사합니다 {self.name}({self.age})님! 의견: {self.comment.value}",
            ephemerial=True
        )

@bot.tree.command(name="feedback")
async def feedback(inter: discord.Interaction):
    await inter.response.send_modal(FeedbackStepOne())
```

모달은 최대 5개의 필드를 포함할 수 있으며, 각 필드는 라벨, 플레이스홀더,
디폴트 값, 스타일, 길이 제한을 지정할 수 있습니다. 긴 텍스트가 필요할 때는
`style=discord.TextStyle.long`를 사용합니다.

## 뷰 수명주기와 권한 검사

`discord.ui.View`는 인터랙션 처리기와 시간 제한을 제어하는 속성을 제공합니다.
`timeout`을 `None`으로 설정하면 영구 뷰가 되어 봇 재시작 후에도 동작합니다.
하지만 영구 뷰의 모든 컴포넌트에는 `custom_id`가 설정되어야 하며, 봇의
`persistent_views` 등록 목록에 추가해야 합니다【716329102970593†L4889-L4924】. 권한을
제한하려면 `interaction_check()` 메서드를 오버라이드하여 `interaction.user`의 역할
또는 ID를 확인합니다. 예:

```python
class RestrictedView(View):
    def __init__(self, allowed_users: set[int]):
        super().__init__(timeout=120)
        self.allowed_users = allowed_users

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        return interaction.user.id in self.allowed_users

    @discord.ui.button(label="비밀 버튼", style=discord.ButtonStyle.primary)
    async def secret(self, _, interaction):
        await interaction.response.send_message("비밀 메시지!", ephemerial=True)
```

이처럼 뷰의 생명주기와 권한을 세밀하게 제어하여 안전하고 사용자 경험이 좋은
인터랙티브 UI를 만들 수 있습니다.

---

다음 장에서는 내부 동시성 도구를 이용한 작업 병렬화와 쓰로틀링 기법을 학습합니다.