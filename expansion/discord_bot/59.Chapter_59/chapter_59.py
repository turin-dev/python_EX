"""버전 관리와 마이그레이션 예제.

이 모듈에서는 설치된 discord.py 버전을 확인하고, 특정 버전
이상의 기능을 요구하는 경우 사용자에게 안내하는 간단한 함수를
제공합니다.
"""

import pkg_resources


def check_version(min_version: str = "2.3.0") -> None:
    """설치된 discord.py 버전을 확인하여 최소 요구 버전보다 낮으면 경고합니다.

    Parameters
    ----------
    min_version: str
        요구하는 최소 버전 문자열.
    """
    try:
        version = pkg_resources.get_distribution("discord.py").version
    except pkg_resources.DistributionNotFound:
        print("discord.py가 설치되어 있지 않습니다. 설치가 필요합니다.")
        return
    from packaging import version as packaging
    if packaging.parse(version) < packaging.parse(min_version):
        print(f"discord.py 버전이 {version}입니다. {min_version} 이상으로 업데이트 하세요.")
    else:
        print(f"discord.py 버전 {version}은 요구사항을 충족합니다.")


if __name__ == "__main__":
    check_version()

