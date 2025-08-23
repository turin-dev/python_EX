# 코그 고급 사용

코그는 기본적인 구조화 기능 외에도 다양한 메타 옵션과 특수 메서드를 통해 동작을 세밀하게 제어할 수 있습니다. 이 장에서는 코그의 메타 클래스를 활용하여 기본 속성을 지정하고, 런타임에 코그를 로드/언로드하는 방법, 그리고 코그 레벨의 체크와 후킹 기능을 다룹니다.

## 1. 메타 클래스와 기본 명령 속성

코그 클래스 안에 `class Meta`를 정의하면, 코그 이름이나 명령어 공통 속성을 미리 지정할 수 있습니다. 예를 들어, 모든 명령어를 비공개(help에서 숨김) 처리하거나 기본 카테고리를 지정할 수 있습니다:

```python
class UtilityCog(commands.Cog, name='유틸리티'):
    class Meta:
        command_attrs = {
            'hidden': False,        # 기본으로 명령어를 숨기지 않음
            'cooldown_after_parsing': False  # 쿨다운 실행 시점 설정 등
        }
```

`name` 매개변수는 코그 이름을 지정하며, 도움말 출력 시 사용됩니다. `command_attrs` 딕셔너리는 코그 내부의 모든 명령어에 기본으로 적용될 키워드 인자를 정의합니다.

## 2. 코그 레벨 체크와 후킹

`Cog.cog_check(self, ctx)` 메서드를 오버라이드하면 코그 내부 모든 명령어에 적용되는 체크를 구현할 수 있습니다. 이 메서드가 `False`를 반환하면 명령이 실행되지 않으며, `commands.CheckFailure` 예외가 발생합니다. 예를 들어, 특정 길드에서만 명령을 허용하는 코그를 만들어 봅니다:

```python
class GuildOnlyCog(commands.Cog):
    def __init__(self, bot, allowed_guild_id):
        self.bot = bot
        self.allowed_guild_id = allowed_guild_id

    async def cog_check(self, ctx):
        return ctx.guild and ctx.guild.id == self.allowed_guild_id

    @commands.command()
    async def secret(self, ctx):
        await ctx.send('해당 길드에서만 사용할 수 있는 명령입니다.')
```

또한 `Cog.cog_before_invoke(self, ctx)`와 `Cog.cog_after_invoke(self, ctx)` 메서드를 오버라이드하면 명령 실행 전후에 공통 로직을 실행할 수 있습니다. 예를 들어 명령이 실행될 때마다 로깅하거나, 실행 시간이 오래 걸리는 명령에는 타임아웃을 적용할 수 있습니다.

## 3. 동적 로딩과 언로드

봇의 기능을 런타임에 변경하려면 **확장(extension)** 을 동적으로 로드하거나 언로드할 수 있습니다. 코그를 모듈 파일로 작성하고 `setup(bot)`에서 등록했다면, 실행 중 다음과 같이 관리 명령을 구현할 수 있습니다:

```python
@bot.command()
@commands.is_owner()
async def reload_cog(ctx, extension: str):
    try:
        bot.unload_extension(extension)
        bot.load_extension(extension)
        await ctx.send(f'{extension}을(를) 새로 고침했습니다.')
    except commands.ExtensionError as e:
        await ctx.send(f'로딩 오류: {e}')
```

`unload_extension()` 호출 시 코그 클래스 내부의 `cog_unload()` 메서드가 존재하면 자동으로 실행되어 정리 작업을 할 수 있습니다【258384405016557†L87-L100】. 예를 들어, 주기적으로 실행되는 태스크를 중지하거나 API 연결을 닫을 수 있습니다.

## 4. 커스텀 헬프 카테고리와 그룹화

`commands.Cog.get_commands()` 메서드를 오버라이드하면 코그가 반환하는 명령어 목록을 수정할 수 있으며, 커스텀 헬프 시스템을 구현할 때 유용합니다. 또한 `command_group()`을 사용해 관련 명령어를 하위 명령 그룹으로 묶어 구조를 더 명확히 할 수 있습니다. 고급 헬프 명령 구현은 후속 장에서 다룹니다.

고급 코그 기능을 활용하면 봇의 구조를 동적으로 변경하고 복잡한 권한 로직을 쉽게 적용할 수 있습니다. 다음 장에서는 백그라운드 작업과 주기적 태스크를 처리하는 방법을 살펴봅니다.



