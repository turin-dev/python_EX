"""이모지와 스티커 관리 예제.

이 모듈에는 길드에 커스텀 이모지를 업로드하거나 삭제하는 기능과
스티커를 보내는 예제 함수가 포함되어 있습니다. 실제 환경에서는
`manage_emojis_and_stickers` 권한이 필요하며, 스티커 업로드는 Nitro
요건을 확인해야 합니다.
"""

import discord


async def upload_custom_emoji(guild: discord.Guild, name: str, image_path: str) -> discord.Emoji:
    """파일을 읽어 커스텀 이모지를 생성하여 반환합니다.

    Parameters
    ----------
    guild: discord.Guild
        이모지를 업로드할 길드 객체.
    name: str
        새 이모지의 이름 (2~32자, 영문/숫자/밑줄).
    image_path: str
        로컬 이미지 파일 경로. PNG/JPEG/GIF, 256KB 이하.
    """
    with open(image_path, "rb") as fp:
        image_data = fp.read()
    emoji = await guild.create_custom_emoji(name=name, image=image_data)
    return emoji


async def list_and_delete_emojis(guild: discord.Guild, delete_if_name: str | None = None) -> list[str]:
    """길드의 모든 이모지를 나열하고, 특정 이름과 일치하면 삭제합니다.

    Returns
    -------
    list[str]
        이모지 이름 목록.
    """
    names: list[str] = []
    for emoji in guild.emojis:
        names.append(emoji.name)
        if delete_if_name and emoji.name == delete_if_name:
            await emoji.delete(reason="자동 삭제")
    return names


async def send_sticker(channel: discord.abc.Messageable, sticker: discord.StickerItem) -> None:
    """지정한 채널에 스티커를 전송합니다."""
    await channel.send(content="스티커 전송 예제입니다", stickers=[sticker])


# 이 모듈은 함수 정의만 포함하며, 실제 봇 코드에서는 위 함수를 호출합니다.

