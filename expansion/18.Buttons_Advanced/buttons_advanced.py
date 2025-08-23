import discord

class AdminView(discord.ui.View):
    def __init__(self, allowed_user: discord.User):
        super().__init__(timeout=None)
        self.allowed_user = allowed_user

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        return interaction.user == self.allowed_user

    @discord.ui.button(label='삭제', style=discord.ButtonStyle.danger, row=0)
    async def delete_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.message.delete()

