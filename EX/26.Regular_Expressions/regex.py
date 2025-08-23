"""예제 26: re 모듈을 사용한 정규 표현식 실습.

이 스크립트는 문자열에서 패턴을 검색하고, 전체 매치 목록을 추출하며,
문자열을 치환하는 다양한 정규 표현식 기능을 보여 준다.
"""

import re


def extract_numbers(text: str) -> list[str]:
    """문자열에서 전화번호 형태의 숫자를 추출한다."""
    pattern = re.compile(r"\b\d{2,3}-\d{3,4}-\d{4}\b")
    return pattern.findall(text)


def anonymize_emails(text: str) -> str:
    """이메일 주소를 [PROTECTED] 형태로 치환한다."""
    email_pattern = re.compile(r"[\w.-]+@[\w.-]+")
    return email_pattern.sub("[PROTECTED]", text)


def split_sentences(text: str) -> list[str]:
    """마침표나 물음표, 느낌표로 구분된 문장 리스트를 반환한다."""
    return re.split(r"[.!?]\s+", text.strip())


if __name__ == '__main__':
    sample = "문의: 010-1234-5678, 대체 번호는 011-987-6543입니다."
    print(extract_numbers(sample))

    text_with_email = "문의는 admin@example.com 또는 support@test.org으로 보내주세요."
    print(anonymize_emails(text_with_email))

    paragraph = "Hello world! This is a test. How are you?"
    print(split_sentences(paragraph))