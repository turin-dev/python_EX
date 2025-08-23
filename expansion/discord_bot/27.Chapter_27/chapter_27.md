# 27장 – 권한과 역할 관리

디스코드 서버에서는 역할(role)과 권한(permission)을 이용해 사용자가 할 수 있는 행동을 제어합니다. 봇 명령을 안전하게 만들려면 특정 권한이나 역할을 가진 사용자만 명령을 실행할 수 있도록 제한해야 합니다. `discord.py`는 명령어 시스템과 슬래시 명령에서 권한을 검증하는 다양한 방법을 제공합니다.

## 프리픽스 명령의 권한 체크

명령어에 데코레이터를 추가해 호출자의 권한이나 역할을 검사할 수 있습니다. `@commands.has_permissions()` 데코레이터는 사용자가 가진 서버 권한(메시지 관리, 밴 등)을 확인하고, `@commands.has_role()`은 특정 역할 이름이나 ID를 요구합니다. 조건을 만족하지 않으면 `MissingPermissions` 또는 `MissingRole` 예외가 발생하며, 이를 처리하는 오류 핸들러를 구현해야 합니다【104993650755089†L47-L112】.

```python
@bot.command()
@commands.has_permissions(manage_messages=True)
async def purge(ctx, limit: int):
    """최근 메시지를 삭제합니다 (메시지 관리 권한 필요)."""
    await ctx.channel.purge(limit=limit)
    await ctx.send(f"{limit}개의 메시지를 삭제했습니다.")

@bot.command()
@commands.has_role("관리자")
async def announce(ctx, *, msg: str):
    await ctx.send(f"공지: {msg}")
```

권한 체크는 복수의 데코레이터를 조합할 수 있으며, 논리 OR가 필요한 경우 `commands.has_any_role()`이나 `@commands.check()`로 커스텀 조건을 구현합니다. 명령이 DM에서 실행되면 서버 권한이 존재하지 않으므로 `@commands.guild_only()`를 추가하는 것도 좋습니다.

## 슬래시 명령의 기본 권한 설정

슬래시 명령에서는 `default_member_permissions` 매개변수로 기본 권한을 지정할 수 있습니다. 예를 들어 메시지 삭제 권한이 있는 멤버만 `/청소` 명령을 실행할 수 있도록 설정하려면:

```python
@bot.tree.command(name="청소", description="메시지를 삭제합니다", default_member_permissions=discord.Permissions(manage_messages=True))
async def clean(interaction: discord.Interaction, count: int):
    await interaction.channel.purge(limit=count)
    await interaction.response.send_message(f"{count}개의 메시지를 삭제했습니다.", ephemeral=True)
```

관리자는 Discord 웹 클라이언트에서 명령어의 권한을 수동으로 변경할 수도 있습니다. 명령어의 가시성을 제한하거나 특정 역할에만 허용하려면 **봇 대시보드**에서 별도로 설정하십시오.

## 역할 부여와 제거

봇으로 역할을 부여하거나 제거하려면 `discord.Member.add_roles()`와 `remove_roles()`를 사용합니다. 예를 들어 특정 명령어로 유료 회원 역할을 추가하는 경우 다음과 같이 구현합니다.

```python
@bot.command()
@commands.has_permissions(manage_roles=True)
async def 가입(ctx, member: discord.Member, role: discord.Role):
    await member.add_roles(role)
    await ctx.send(f"{member.display_name}님에게 {role.name} 역할을 부여했습니다.")
```

역할을 다룰 때는 봇 계정의 역할 위치가 대상 역할보다 위에 있어야 하며, 그렇지 않으면 `Forbidden` 예외가 발생합니다. 또한 역할과 권한을 조합해 섬세한 제어를 구현할 수 있습니다.

## 요약

권한과 역할 관리는 서버 보안과 질서를 유지하는 핵심 요소입니다. 데코레이터를 사용해 명령어에 권한 체크를 추가하고, 슬래시 명령에서도 기본 권한을 설정하여 무분별한 사용을 방지하세요. 역할을 부여하거나 제거할 때는 봇의 권한과 역할 순서를 확인하는 것도 잊지 마세요.

