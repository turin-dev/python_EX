# 제77장 – 고급 가비지 컬렉션 제어

파이썬의 메모리 관리는 참조 카운팅과 순환 참조를 탐지하는 세대별 가비지 컬렉터로 구성되어 있습니다. `gc` 모듈은 수집기의 상태를 검사하고 조정하는 함수를 제공합니다. 자동 수집을 비활성화하거나 컬렉션을 트리거하는 임계값을 조정하고, 컬렉션 활동을 관찰하기 위한 디버그 플래그를 설정할 수 있습니다【721861822603243†L49-L57】.

## 세대별 임계값

가비지 컬렉터는 객체를 세 개의 세대로 나눕니다. 한 세대의 할당 수에서 해제 수를 뺀 값이 임계값을 초과하면 그 세대와 더 어린 세대에서 컬렉션이 실행됩니다. `gc.get_threshold()`로 현재 임계값을 확인하고, `gc.set_threshold(threshold0, threshold1, threshold2)`로 변경할 수 있습니다. 임계값을 낮추면 더 자주 컬렉션을 실행하지만 오버헤드가 증가하고, 높이면 메모리 사용량은 늘어날 수 있지만 컬렉션 횟수가 줄어듭니다.

```python
import gc

print("Current thresholds:", gc.get_threshold())
# 컬렉션 횟수를 줄이기 위해 임계값을 두 배로 설정
current = gc.get_threshold()
gc.set_threshold(current[0] * 2, current[1] * 2, current[2] * 2)
print("Updated thresholds:", gc.get_threshold())
```

## 컬렉션 활동 디버깅

`gc.set_debug(flags)`를 호출하여 컬렉션 시 진단 정보를 출력하도록 디버그 플래그를 설정할 수 있습니다. `gc.DEBUG_STATS`, `gc.DEBUG_COLLECTABLE`, `gc.DEBUG_UNCOLLECTABLE` 등의 플래그가 있습니다. 디버깅이 끝나면 디버그 플래그를 0으로 설정해 출력을 중지합니다. 디버깅은 `__del__` 메서드나 참조 사이클로 인해 수집되지 않는 객체를 찾는 데 도움이 됩니다.

```python
import gc

gc.set_debug(gc.DEBUG_UNCOLLECTABLE | gc.DEBUG_STATS)
# 객체를 할당하고 컬렉션을 강제로 수행
gc.collect()
gc.set_debug(0)
```

## 요약

컬렉션 임계값을 조정하고 디버그 플래그를 설정하여 가비지 컬렉터를 세밀하게 조정할 수 있습니다. GC 동작을 제어하면 성능을 개선하고 메모리 누수를 진단하는 데 도움을 줍니다【721861822603243†L49-L57】.