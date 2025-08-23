# 임베드와 리치 메시지 디자인

기본 텍스트 메시지만으로는 정보 전달에 한계가 있습니다. **임베드(Embed)**는
제목, 설명, 필드, 이미지, 썸네일, 저자 등 다양한 요소를 포함할 수 있어
메시지를 아름답게 꾸밀 수 있습니다. 또한 버튼과 셀렉트 메뉴를 결합해
인터랙티브한 리치 메시지를 만들 수 있습니다. 이 장에서는 임베드를 설계하고
사용자 경험을 높이는 디자인 패턴을 살펴봅니다.

## Embed 구성 요소

임베드는 색상(`color`), 제목(`title`), 설명(`description`), URL(`url`),
작성자(`set_author()`), 썸네일(`set_thumbnail()`), 이미지(`set_image()`),
푸터(`set_footer()`), 필드(`add_field()`) 등으로 구성됩니다. 모든 요소는
선택적이며, 6000자 제한 내에서 최대 25개의 필드를 포함할 수 있습니다.

```python
embed = discord.Embed(
    title="공지사항",
    description="새로운 기능이 추가되었습니다!",
    color=discord.Color.blue(),
)
embed.set_author(name="관리자", icon_url=ctx.guild.icon)
embed.set_thumbnail(url="https://example.com/thumb.png")
embed.add_field(name="기능 1", value="자세한 설명...", inline=False)
embed.add_field(name="기능 2", value="더보기...", inline=True)
embed.set_footer(text="업데이트 날짜: 2025-08-23")
await ctx.send(embed=embed)
```

컬러는 헥스 코드(`discord.Color.from_str("#7289DA")`)나 미리 정의된 색을 사용할 수 있습니다. 이미지와 썸네일은 URL 또는 `discord.File`로 첨부할 수 있으며, Discord가 지원하는 형식이어야 합니다.

## 임베드와 UI 컴포넌트 결합

임베드는 버튼과 셀렉트 메뉴를 함께 사용해 풍부한 인터페이스를 구현할 수 있습니다. 예를 들어 여러 페이지로 구성된 가이드를 제공할 때 버튼을 사용해 페이지를 이동하거나, 셀렉트 메뉴로 카테고리를 선택하도록 할 수 있습니다. 버튼은 최대 5개까지 한 행(row)에 배치할 수 있으며【716329102970593†L5969-L6031】, 여러 행을 조합해 최대 5×5 버튼을 만들 수 있습니다.

```python
class HelpView(discord.ui.View):
    def __init__(self, pages: list[discord.Embed]):
        super().__init__(timeout=120)
        self.pages = pages
        self.index = 0

    async def update(self, inter: discord.Interaction):
        await inter.response.edit_message(embed=self.pages[self.index], view=self)

    @discord.ui.button(label="◀", style=discord.ButtonStyle.secondary)
    async def prev(self, _, inter):
        self.index = (self.index - 1) % len(self.pages)
        await self.update(inter)

    @discord.ui.button(label="▶", style=discord.ButtonStyle.secondary)
    async def next(self, _, inter):
        self.index = (self.index + 1) % len(self.pages)
        await self.update(inter)

@bot.command()
async def help(ctx):
    pages = [discord.Embed(title=f"도움말 {i+1}", description=f"내용 {i+1}") for i in range(3)]
    view = HelpView(pages)
    await ctx.send(embed=pages[0], view=view)
```

위 예제에서 페이지를 저장한 후 버튼 콜백에서 인덱스를 변경하고 메시지를
편집합니다. `View`의 `timeout`을 설정해 일정 시간 후에는 버튼이 비활성화되도록
할 수 있습니다. persistent view로 만들려면 앞서 설명한 조건을 충족해야
합니다【716329102970593†L4889-L4924】.

## 메시지 첨부파일과 Embed 이미지

파일을 첨부하면서 임베드에 이미지를 넣고 싶다면 `discord.File`과 `embed.set_image(file=...)`를 함께 사용합니다. Discord는 최대 8MB(서버에 따라 다를 수 있음)까지
첨부를 허용합니다.

```python
file = discord.File("./images/banner.png", filename="banner.png")
embed = discord.Embed(title="배너 테스트")
embed.set_image(url="attachment://banner.png")
await ctx.send(file=file, embed=embed)
```

## 독창적인 디자인 팁

- **읽기 쉬움**: 필드를 너무 많이 나열하지 말고, 긴 문장은 설명에 작성합니다.
- **상징적인 색상**: 서버의 브랜드 컬러를 사용하거나 메시지의 성격에 따라 색상을 바꿉니다.
- **미디어 활용**: 썸네일과 이미지는 관련성을 유지하면서 시각적 흥미를 높입니다.
- **일관성**: 모든 임베드에 동일한 푸터나 작성자 정보를 넣어 브랜드 통일성을 유지합니다.

---

이번 장에서는 임베드를 활용한 리치 메시지 디자인과 UI 컴포넌트 조합을 살펴보았습니다. 다음 장에서는 여러 길드의 데이터를 통합하여 글로벌 리더보드와 같은 기능을 만드는 방법을 알아봅니다.