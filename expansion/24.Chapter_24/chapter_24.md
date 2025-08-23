# 24장 – 데이터 저장과 파일 I/O

디스코드 봇은 사용자 설정, 통계, 역할 목록 등 영속적으로 저장해야 하는 데이터를 다루는 경우가 많습니다. 가장 간단한 방법은 JSON, CSV와 같은 파일 포맷을 사용하여 데이터를 로컬에 저장하고 읽는 것입니다. 이 장에서는 파이썬의 `json` 모듈을 이용한 데이터 직렬화 및 역직렬화, 비동기 파일 I/O, 그리고 간단한 데이터베이스 접근에 대해 설명합니다.

## JSON을 이용한 설정 저장

JSON 포맷은 키–값 형태의 데이터를 표현하기에 적합합니다. 사용자 설정을 저장하려면 명령어 실행 시 필요한 값을 딕셔너리에 저장하고, 프로그램 종료 전 또는 명령 처리 직후 파일에 기록하면 됩니다. 파일을 열 때는 항상 UTF-8 인코딩을 명시하고 예외를 처리해야 합니다.

```python
import json
from pathlib import Path

CONFIG_FILE = Path("config.json")

def load_config() -> dict:
    if CONFIG_FILE.exists():
        with CONFIG_FILE.open("r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_config(data: dict) -> None:
    with CONFIG_FILE.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

# 봇 실행 시 설정을 로드
config = load_config()
config.setdefault("greeting", "안녕!")

```

명령어 핸들러 내부에서 설정 값을 수정한 뒤 `save_config(config)`를 호출하면 변경사항이 파일에 반영됩니다. 다중 프로세스 환경에서는 동시 쓰기로 인한 손상 방지를 위해 락이나 데이터베이스를 사용하는 것이 안전합니다.

## 비동기 파일 I/O

큰 파일을 읽거나 네트워크 I/O를 병렬로 처리할 때는 비동기 I/O를 사용하는 것이 효율적입니다. `aiofiles` 라이브러리를 설치하면 `async with` 구문을 사용해 파일을 비동기적으로 읽고 쓸 수 있습니다. 다음은 채널의 메시지를 로그 파일에 비동기적으로 기록하는 예입니다.

```python
import aiofiles

@bot.command()
async def log_message(ctx, *, content: str):
    async with aiofiles.open("messages.log", "a", encoding="utf-8") as f:
        await f.write(content + "\n")
    await ctx.send("메시지가 저장되었습니다.")
```

## 간단한 데이터베이스 사용

파일 저장이 복잡해질 경우, SQLite와 같은 경량 데이터베이스를 사용하는 것이 좋습니다. Python 표준 라이브러리의 `sqlite3` 모듈을 통해 파일 기반의 SQL 데이터베이스에 접근할 수 있습니다. 자세한 내용은 일반 파이썬 학습 자료에서 다루었으므로 여기서는 생략하지만, 데이터 무결성과 동시성을 위해 트랜잭션을 활용하는 것이 중요합니다【232817957113109†L82-L92】.

## 요약

작은 규모의 봇에서는 JSON 파일과 같은 단순한 저장 방식으로도 데이터를 관리할 수 있습니다. 중요한 것은 파일 접근 시 인코딩과 예외를 관리하고, 다중 호출 환경에서 데이터 손상에 주의하는 것입니다. 복잡한 상태를 저장해야 한다면 SQLite나 외부 데이터베이스를 도입하는 것도 고려할 수 있습니다.

