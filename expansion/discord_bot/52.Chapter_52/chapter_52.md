# 이모지와 스티커 관리

이모지와 스티커는 서버의 분위기를 살리고 커뮤니케이션을 풍성하게 만들어 줍니다. 봇을 통해 이모지를 업로드하거나 삭제하고, 스티커를 관리하는 방법을 알아봅니다. 또한 메시지에 이모지와 스티커를 사용하는 법과 권한 요구 사항을 설명합니다.

## 커스텀 이모지 업로드

길드(서버)에서는 고유한 커스텀 이모지를 업로드할 수 있습니다. 이를 위해서는 **`manage_emojis_and_stickers` 권한**이 필요합니다. 다음 함수는 로컬 이미지 파일을 읽어 `discord.Guild` 객체의 `create_custom_emoji` 메서드를 사용해 이모지를 업로드합니다. 업로드 가능한 포맷은 PNG, JPEG, GIF 등이며 파일 크기는 256KB 이하로 제한됩니다.

```python
import discord

async def upload_custom_emoji(guild: discord.Guild, name: str, image_path: str) -> discord.Emoji:
    """이미지 파일을 업로드하여 커스텀 이모지를 생성합니다."""
    with open(image_path, "rb") as f:
        img_data = f.read()
    emoji = await guild.create_custom_emoji(name=name, image=img_data)
    return emoji
```

업로드 후에는 `emoji` 객체를 메시지에 `str(emoji)` 형식으로 삽입하여 사용할 수 있습니다. 예를 들어, `await channel.send(f"{emoji} 축하합니다!")`처럼 사용할 수 있습니다.

### 이모지 나열 및 삭제

길드의 모든 이모지는 `guild.emojis` 속성에서 확인할 수 있습니다. 특정 이모지를 삭제하려면 `await emoji.delete()`를 호출합니다. 이때도 `manage_emojis_and_stickers` 권한이 필요합니다.

## 스티커 관리

스티커는 이모지보다 큰 그림으로, 애니메이션이나 APNG 형식일 수 있습니다. `discord.py`에서는 길드의 `create_sticker` 메서드를 통해 스티커를 업로드할 수 있지만, Nitro 구독과 특정 포맷 요건이 필요합니다. 스티커를 보낼 때는 `await channel.send(stickers=[sticker])`처럼 리스트로 전달해야 합니다.

스티커 파일은 PNG/APNG(최대 500KB) 또는 Lottie(JSON) 형식이며, 서브커맨드 `emoji create` 대신 `/sticker` 명령으로 업로드합니다. 봇 코드에서 스티커를 보내는 예제는 다음과 같습니다:

```python
async def send_sticker(channel: discord.TextChannel, sticker: discord.StickerItem) -> None:
    await channel.send(content="이건 재미있는 스티커입니다!", stickers=[sticker])
```

## 권한과 주의 사항

- **업로드/삭제 권한**: `manage_emojis_and_stickers` 권한이 있어야 하며, 일부 서버에서는 관리자만 가능합니다.
- **저작권**: 이미지·스티커 파일은 저작권을 준수해야 합니다. 무단 업로드 시 계정이 제한될 수 있습니다.
- **이모지 이름**: 영어 소문자와 숫자, 밑줄만 사용할 수 있고 길이는 2~32자입니다.

이모지와 스티커를 적절히 활용하면 서버에 개성을 더할 수 있습니다. 하지만 권한과 파일 크기 제한을 고려하여 관리해야 합니다.

\[타이머와 루프 기능 참조\]【230406618874054†L160-L210】

