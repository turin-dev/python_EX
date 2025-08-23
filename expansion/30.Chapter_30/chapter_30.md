# 30장 – 확장 및 코그 재로드

봇의 기능이 늘어나면 명령과 이벤트를 여러 파일로 나누어 관리하는 것이 좋습니다. `discord.py`에서는 **확장(Extension)** 과 **코그(Cog)** 를 동적으로 로드하고 언로드하며, 개발 중에도 코드를 수정한 뒤 봇을 재시작하지 않고 새로 고칠 수 있습니다. 이 장에서는 확장을 로딩/언로드/재로드하는 방법과 간단한 관리 명령을 구현하는 방법을 소개합니다.

## 확장 로딩과 언로드

확장은 Python 모듈로, 내부에 코그를 포함하거나 다른 초기화를 수행할 수 있습니다. `commands.Bot`의 `load_extension()` 메서드는 모듈을 임포트하여 `setup(bot)` 함수를 실행합니다. 언로드할 때는 `unload_extension()`을 사용하여 등록된 명령과 리스너를 제거합니다.

```python
@bot.command()
@commands.is_owner()
async def reload(ctx, extension: str):
    """지정한 확장을 재로드합니다 (오너 전용)."""
    try:
        bot.reload_extension(extension)
    except commands.ExtensionNotLoaded:
        await ctx.send("확장이 로드되지 않았습니다. 먼저 load 명령을 사용하세요.")
    except commands.ExtensionFailed as e:
        await ctx.send(f"재로드 실패: {e}")
    else:
        await ctx.send(f"{extension} 확장이 재로드되었습니다.")
```

위 명령은 `/` 슬래시 명령으로도 구현할 수 있으며, 오너나 관리자만 사용 가능하도록 `@commands.is_owner()` 또는 `default_member_permissions`를 지정하는 것이 안전합니다.

## 핫 리로드 자동화

개발 단계에서는 파일 변경을 감지해 자동으로 확장을 재로드하면 편리합니다. `watchdog` 등의 라이브러리를 사용해 파일 시스템 이벤트를 감지한 뒤 `bot.reload_extension()`을 호출할 수 있습니다. 단, 재로드 시 상태가 초기화되므로 전역 변수나 태스크 루프의 상태를 복구하는 로직을 추가해야 합니다. 또한 싱글톤 객체나 외부 연결(데이터베이스, HTTP 세션 등)을 다시 생성해야 할 수 있습니다.

## 요약

확장과 코그를 나누어 관리하면 프로젝트 구조를 체계적으로 유지할 수 있으며, 문제 발생 시 해당 모듈만 언로드하거나 재로드할 수 있습니다. `reload_extension()` 명령을 구현해 수정 사항을 즉시 적용하고, 개발 중에는 파일 감지 도구를 활용해 자동 재시작을 할 수 있습니다. 이러한 관리 도구를 통해 봇 개발과 유지보수가 훨씬 수월해집니다【258384405016557†L27-L44】.

