"""설정 파일 관리 예제 (JSON 및 YAML).

이 모듈은 JSON 및 YAML 형식의 설정 파일을 읽고 저장하는 함수를
제공합니다. YAML 처리를 위해서는 PyYAML 패키지가 필요합니다.
"""

import json
import yaml
from typing import Any, Dict


def load_json(path: str) -> Dict[str, Any]:
    """JSON 파일을 읽어 딕셔너리를 반환합니다."""
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json(path: str, data: Dict[str, Any]) -> None:
    """딕셔너리를 JSON 파일로 저장합니다."""
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def load_yaml(path: str) -> Dict[str, Any]:
    """YAML 파일을 읽어 딕셔너리를 반환합니다."""
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def save_yaml(path: str, data: Dict[str, Any]) -> None:
    """딕셔너리를 YAML 파일로 저장합니다."""
    with open(path, "w", encoding="utf-8") as f:
        yaml.safe_dump(data, f, allow_unicode=True)

