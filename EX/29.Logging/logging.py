"""예제 29: logging 모듈을 사용한 로깅 설정과 사용.

이 스크립트는 기본 구성과 사용자 정의 핸들러를 사용하여 다양한 로깅 메시지를 출력하는
방법을 보여 준다.
"""

import logging


def basic_logging() -> None:
    """루트 로거를 간단하게 구성하여 메시지를 기록한다."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    )
    logger = logging.getLogger(__name__)
    logger.info("This is an info message")
    logger.warning("This is a warning")
    logger.error("This is an error message")


def custom_logging() -> None:
    """파일 핸들러와 포매터를 직접 추가하여 로깅을 커스터마이즈한다."""
    logger = logging.getLogger('myapp')
    logger.setLevel(logging.DEBUG)
    # 콘솔 핸들러
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(logging.Formatter('[%(levelname)s] %(message)s'))
    # 파일 핸들러
    file_handler = logging.FileHandler('myapp.log')
    file_handler.setLevel(logging.ERROR)
    file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s'))
    # 핸들러 추가
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    # 로깅 사용
    logger.debug('디버그 메시지')
    logger.info('정보 메시지')
    logger.error('오류 발생!')
    logger.critical('치명적 오류 발생!')


if __name__ == '__main__':
    basic_logging()
    print('--- Custom logging ---')
    custom_logging()