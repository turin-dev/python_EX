# 설정 파일 관리 (JSON/YAML)

봇의 동작을 사용자나 운영자가 쉽게 수정할 수 있도록 설정을 외부 파일에 저장하는 것이 좋습니다. 일반적으로 **JSON**과 **YAML** 형식이 사용됩니다. JSON은 파이썬 표준 라이브러리에 `json` 모듈이 포함되어 있어 간편하며, YAML은 가독성이 좋아 사람이 편하게 편집할 수 있습니다.

## JSON 설정 파일

JSON은 키-값 구조를 사용해 설정을 표현합니다. 다음은 간단한 설정 파일(`config.json`)의 예입니다:

```json
{
  "prefix": "!",
  "admin_roles": [123456789012345678],
  "log_channel": 987654321098765432
}
```

파이썬에서는 `json` 모듈로 손쉽게 읽고 쓸 수 있습니다:

```python
import json

def load_config(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def save_config(path: str, data: dict) -> None:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

# 사용 예
config = load_config("config.json")
config["prefix"] = "?"
save_config("config.json", config)
```

## YAML 설정 파일

YAML은 들여쓰기로 구조를 표현해 가독성이 좋습니다. YAML을 사용하려면 `PyYAML` 패키지를 설치해야 합니다. YAML 파일(`config.yaml`) 예시는 다음과 같습니다:

```yaml
prefix: '!'
admin_roles:
  - 123456789012345678
log_channel: 987654321098765432
```

YAML 파일을 읽고 쓰려면 `yaml.safe_load()`와 `yaml.safe_dump()`를 사용합니다:

```python
import yaml

def load_yaml(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def save_yaml(path: str, data: dict) -> None:
    with open(path, "w", encoding="utf-8") as f:
        yaml.safe_dump(data, f, allow_unicode=True)
```

## 주의 사항

- 설정 파일에 비밀 값을 저장할 때는 파일 권한을 적절히 설정하거나 별도의 비밀 관리 시스템과 결합하는 것이 좋습니다.
- YAML은 주석을 지원하지만 JSON은 주석을 허용하지 않으므로, 주석이 필요하다면 YAML을 선택할 수 있습니다.
- 구성 데이터를 코드에서 직접 수정할 때는 충돌을 방지하기 위해 잠금(lock)이나 백업 전략을 마련합니다.

설정 파일을 활용하면 봇의 동작을 코드 수정 없이도 유연하게 변경할 수 있어 운영에 편리합니다.

