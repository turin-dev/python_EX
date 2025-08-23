"""테스트와 디버깅 예제.

간단한 함수에 대한 `unittest` 테스트를 정의하고, 비동기 봇 명령을 테스트하기 위한 예제를 제공합니다.
"""

import unittest
import asyncio
import discord
from discord.ext import commands


def add(a: int, b: int) -> int:
    """두 정수를 더합니다."""
    return a + b


class TestAdd(unittest.TestCase):
    """add 함수에 대한 단위 테스트."""

    def test_add(self) -> None:
        self.assertEqual(add(2, 3), 5)
        self.assertNotEqual(add(2, 2), 5)


# 비동기 명령 테스트 예제
async def ping(ctx: commands.Context) -> None:
    await ctx.send("pong")


async def test_ping_command() -> None:
    """비동기 명령 테스트를 수동으로 실행하는 예제."""
    # 모의 컨텍스트를 만들어 비동기 함수를 호출할 수 있습니다.
    class MockContext:
        async def send(self, msg: str) -> None:
            print(msg)  # 실제 테스트에서는 값을 어딘가 저장하여 검증합니다.

    ctx = MockContext()
    await ping(ctx)


if __name__ == "__main__":
    # unittest를 실행합니다.
    unittest.main(exit=False)
    # 비동기 테스트 실행
    asyncio.run(test_ping_command())