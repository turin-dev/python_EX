"""예제 31: 가상 환경(`venv`)에서 실행되는지 확인.

이 스크립트는 현재 파이썬 인터프리터의 기본 경로를 출력하여 가상 환경 여부를
확인한다. 실제 가상 환경 생성과 활성화는 쉘에서 수행해야 한다.
"""

import sys
import os


def is_venv() -> bool:
    """현재 실행 중인 인터프리터가 가상 환경에 있는지 여부를 반환한다."""
    # 가상 환경에서는 sys.prefix가 시스템 prefix와 다르며, VIRTUAL_ENV 환경 변수가 설정된다.
    return (
        hasattr(sys, 'real_prefix') or
        (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix) or
        'VIRTUAL_ENV' in os.environ
    )


if __name__ == '__main__':
    if is_venv():
        print('This Python is running inside a virtual environment.')
        print('sys.prefix:', sys.prefix)
    else:
        print('This Python is NOT in a virtual environment.')
        print('sys.prefix:', sys.prefix)