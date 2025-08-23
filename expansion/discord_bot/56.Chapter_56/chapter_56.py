"""지속 뷰와 상태 유지 예제.

이 모듈에는 봇 재시작 후에도 작동하는 지속 뷰를 구현하는 예제가
포함되어 있습니다. ToggleRoleView는 버튼을 클릭할 때마다 지정한
역할을 사용자에게 토글하며, 뷰는 timeout=None으로 지정되어 만료되지
않습니다. 봇이 시작될 때 `bot.add_view()`를 호출하여 뷰를 등록해야
합니다.
"""

import discord
from discord.ext import commands


class ToggleRoleView(discord.ui.View):
    """사용자 역할을 토글하는 지속 뷰.

    Parameters
    ----------
    role_id: int
        토글할 역할의 ID.
    """

    def __init__(self, role_id: int) -> None:
        super().__init__(timeout=None)
        self.role_id = role_id

        # TODO: 아래 메서드를 구현하여 버튼 클릭 시 역할을 토글하세요.
        # 예:
        # @discord.ui.button(label="역할 토글", custom_id="toggle_role", style=discord.ButtonStyle.success)
        # async def toggle_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        #     # role = interaction.guild.get_role(self.role_id)
        #     # if role in interaction.user.roles:
        #     #     await interaction.user.remove_roles(role)
        #     # else:
        #     #     await interaction.user.add_roles(role)
        #     # await interaction.response.send_message(..., ephemeral=True)

