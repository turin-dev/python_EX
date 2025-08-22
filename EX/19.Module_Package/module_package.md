---

# 모듈과 패키지

## 모듈(module)

- 파이썬 코드가 저장된 `.py` 파일을 모듈이라고 합니다.
- `import 모듈명`을 사용하여 다른 모듈의 함수나 클래스 등을 가져올 수 있습니다.
- 모듈의 일부만 사용하려면 `from 모듈명 import 이름` 문을 사용합니다.

```python
import math
print(math.sqrt(16))

from datetime import datetime
print(datetime.now())
```

## 표준 라이브러리

- Python은 풍부한 표준 라이브러리를 제공하며, 파일 처리, 웹 통신, 데이터 구조 등 다양한 모듈을 포함합니다.
- 필요한 기능을 찾을 때 표준 라이브러리를 먼저 확인하는 것이 좋습니다.

## 패키지(package)

- 모듈의 집합으로, 디렉터리 구조를 사용하여 여러 모듈을 체계적으로 관리합니다.
- 패키지는 `__init__.py` 파일을 포함하여 해당 디렉터리를 패키지로 인식시킵니다.
- 서브패키지를 중첩하여 구조화할 수 있습니다. 예: `package.subpackage.module`.

## `__name__ == "__main__"` 패턴

- 모듈이 다른 모듈에 import될 때는 실행되지 않고, 스크립트로 직접 실행될 때만 특정 코드가 실행되도록 하는 관용적 패턴입니다.

```python
def main():
    print("스크립트 실행")

if __name__ == "__main__":
    main()
```

## 요약

모듈과 패키지를 활용하면 코드를 기능별로 분리하고 재사용할 수 있습니다. 표준 라이브러리와 외부 패키지를 적절히 활용하여 프로그램의 생산성을 높여 보세요.

## 추가 설명

### 절대 import와 상대 import

다른 모듈을 가져올 때는 절대 경로(`package.module`)를 사용할 수도 있고, 현재 패키지를 기준으로 점(`.`)을 이용한 상대 import를 사용할 수도 있습니다. 상대 import는 패키지 내부 구조가 바뀔 때 함께 수정되므로, 내부 모듈 간에 자주 사용됩니다. 예: `from .submodule import func`.

### 별칭과 공개 API 제어

`as` 키워드를 사용하면 모듈이나 함수에 짧은 이름을 부여할 수 있습니다: `import numpy as np`. 패키지의 `__init__.py` 파일에 `__all__` 리스트를 정의하면 `from package import *`가 가져오는 공개 API를 제어할 수 있습니다.

### importlib과 동적 로딩

`importlib` 모듈을 사용하면 문자열로 된 모듈 이름을 동적으로 import할 수 있습니다. 예를 들어 플러그인 시스템에서 모듈 이름을 런타임에 결정할 때 유용합니다.

```python
import importlib
math_module = importlib.import_module('math')
print(math_module.sqrt(9))
```

### 패키지 배포와 가상 환경

외부 패키지는 `pip`를 통해 설치할 수 있습니다. 패키지를 배포하려면 `pyproject.toml`과 `setup.cfg`를 작성하여 메타데이터를 제공해야 합니다. 프로젝트마다 독립적인 의존성을 유지하려면 `python -m venv venv`로 가상 환경을 만들고 `source venv/bin/activate`로 활성화하세요.