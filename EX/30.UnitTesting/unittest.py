"""예제 30: unittest 모듈을 이용한 단위 테스트 작성.

이 파일은 간단한 함수에 대한 테스트 케이스를 정의하고, 테스트 스위트를
수동으로 실행하는 예를 보여 준다.
"""

import unittest


def multiply(a: int, b: int) -> int:
    """두 값을 곱한다."""
    return a * b


class MultiplyTestCase(unittest.TestCase):
    def setUp(self) -> None:
        print('setUp called')

    def tearDown(self) -> None:
        print('tearDown called')

    def test_multiply_positive(self) -> None:
        self.assertEqual(multiply(3, 4), 12)

    def test_multiply_zero(self) -> None:
        self.assertEqual(multiply(0, 5), 0)

    def test_multiply_negative(self) -> None:
        self.assertEqual(multiply(-2, 6), -12)


def suite() -> unittest.TestSuite:
    s = unittest.TestSuite()
    s.addTest(MultiplyTestCase('test_multiply_positive'))
    s.addTest(MultiplyTestCase('test_multiply_zero'))
    s.addTest(MultiplyTestCase('test_multiply_negative'))
    return s


if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())