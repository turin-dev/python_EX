# 모듈과 패키지 사용 예제

import math
from datetime import datetime

def main():
    print('sqrt(16) =', math.sqrt(16))
    print('현재 시간:', datetime.now())


if __name__ == "__main__":
    main()

    # 별칭 import와 importlib 동적 로딩 예제
    import math as m
    print('cos(0) =', m.cos(0))

    import importlib
    json_module = importlib.import_module('json')
    print('dumps:', json_module.dumps({'a': 1}))