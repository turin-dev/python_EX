# 제66장 – 동적 임포트와 패키지 메타데이터

파이썬의 임포트 시스템은 확장 가능하며 `importlib` 모듈은 임포트 메커니즘의 이식 가능한 구현을 제공하고 커스텀 임포터에 필요한 구성 요소를 노출합니다. 문서에서는 프로그램적으로 모듈을 로드할 때 내장 `__import__()` 대신 `importlib.import_module()`을 사용하라고 권장합니다【491628540515688†L69-L84】. 또한 `importlib.metadata`를 통해 패키지를 임포트하지 않고도 버전과 메타데이터에 접근할 수 있습니다.

## 동적 임포트

런타임에 이름이 결정되는 모듈을 임포트하려면 `importlib.import_module(name)`을 호출합니다. 점으로 구분된 이름을 사용하면 서브패키지나 서브모듈을 임포트할 수 있습니다. `pkgutil.iter_modules()`나 `importlib.resources.files()`와 결합해 플러그인을 동적으로 탐색하고 로드할 수 있습니다.

```python
import importlib

def load_and_run(module_name: str, func_name: str) -> None:
    module = importlib.import_module(module_name)
    func = getattr(module, func_name)
    result = func()
    print(f"{module_name}.{func_name} returned {result}")

load_and_run("math", "sqrt")
```

## 패키지 메타데이터

`importlib.metadata` API(파이썬 3.8 도입)를 사용하면 패키지를 임포트하지 않고도 설치된 배포판의 정보를 조회할 수 있습니다. `version()`으로 패키지 버전 문자열을 얻고, `metadata()`나 `metadata.distribution()`으로 작성자, 라이선스, 엔트리 포인트 등 메타데이터 필드를 조회합니다.

```python
from importlib.metadata import version, metadata

print("Pip version:", version("pip"))
meta = metadata("pip")
print(meta["Summary"])  # 패키지 요약 설명
```

## 패키징 가이드라인

현대 파이썬 패키징은 `pyproject.toml` 파일을 사용해 빌드 요구사항과 메타데이터를 선언합니다. `setuptools`, `flit`, `poetry` 같은 도구는 이 파일을 읽어 휠을 빌드합니다. `importlib.metadata`를 이용해 의존성과 엔트리 포인트를 확인할 수 있습니다.

## 요약

동적 임포트에는 `__import__()` 대신 `importlib.import_module()`을 사용하세요【491628540515688†L69-L84】. 패키지를 임포트하지 않고 버전과 메타데이터를 조회하려면 `importlib.metadata`를 사용합니다. 패키징은 `pyproject.toml`을 중심으로 선언형 빌드로 발전하고 있습니다.