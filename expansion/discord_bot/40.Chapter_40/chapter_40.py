"""자동완성과 선택지 예제.

고정 선택지와 동적 자동완성을 사용하는 슬래시 명령을 구현합니다.
"""

import discord
from discord import app_commands
from discord.ext import commands


bot = commands.Bot(command_prefix="!", intents=discord.Intents.default())


@bot.tree.command(name="color", description="색상을 선택합니다")
@app_commands.choices(
    colour=[
        app_commands.Choice(name="빨강", value=1),
        app_commands.Choice(name="초록", value=2),
        app_commands.Choice(name="파랑", value=3),
    ]
)
async def color_slash(interaction: discord.Interaction, colour: app_commands.Choice[int]) -> None:
    await interaction.response.send_message(f"선택한 색상: {colour.name}")


@app_commands.command(name="dm", description="사용자에게 DM을 보냅니다")
@app_commands.autocomplete(
    member=lambda interaction, current: [
        app_commands.Choice(name=member.display_name, value=str(member.id))
        for member in interaction.guild.members
        if current.lower() in member.display_name.lower()
    ][:25]
)
async def dm_slash(interaction: discord.Interaction, member: discord.Member, *, message: str) -> None:
    await member.send(message)
    await interaction.response.send_message("DM을 전송했습니다", ephemeral=True)


@bot.event
async def on_ready() -> None:
    await bot.tree.sync()
    print("명령어가 동기화되었습니다.")


if __name__ == "__main__":
    # bot.run("YOUR_TOKEN")
    pass