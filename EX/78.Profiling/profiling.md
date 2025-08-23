# 제78장 – 성능 측정과 프로파일링

성능을 분석하면 병목 현상을 찾아내고 코드를 최적화할 수 있습니다. `timeit` 모듈은 짧은 파이썬 코드 조각을 측정하기 위한 간단한 방법을 제공합니다【19128105459207†L59-L63】. 보다 포괄적인 프로파일링을 위해서는 `cProfile`로 함수 호출 통계를 수집하고 `pstats`로 결과를 분석할 수 있습니다.

## `timeit`으로 실행 시간 측정

`timeit.timeit(stmt, setup, number)`는 주어진 문장을 여러 번 실행하고 총 시간을 반환합니다. 타이밍 중에는 가비지 컬렉터를 비활성화하여 노이즈를 줄입니다. 명령줄에서 `python -m timeit <문장>`을 실행할 수도 있습니다【19128105459207†L59-L63】.

```python
import timeit

code = "sorted(range(1000), reverse=True)"
duration = timeit.timeit(code, number=1000)
print(f"Executed in {duration:.4f} seconds")
```

## `cProfile`로 프로파일링

`cProfile`은 함수 호출 횟수와 누적 시간을 포함한 통계를 수집합니다. 스크립트를 `python -m cProfile script.py`로 실행하거나 프로그래밍 방식으로 특정 함수를 프로파일링할 수 있습니다.

```python
import cProfile
import pstats
from functools import lru_cache

@lru_cache(maxsize=None)
def fib(n):
    return n if n < 2 else fib(n-1) + fib(n-2)

profiler = cProfile.Profile()
profiler.enable()
fib(20)
profiler.disable()
pstats.Stats(profiler).sort_stats('cumulative').print_stats(5)
```

## 요약

작은 코드 스니펫을 빠르게 벤치마킹하려면 `timeit`을 사용하세요【19128105459207†L59-L63】. 프로그램 전체를 분석하고 어떤 함수가 가장 많은 시간을 소비하는지 파악하려면 `cProfile`과 `pstats`를 사용해 프로파일링하세요.