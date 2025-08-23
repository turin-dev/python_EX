import discord

class FeedbackModal(discord.ui.Modal, title='피드백 폼'):
    feedback = discord.ui.TextInput(label='피드백', style=discord.TextStyle.paragraph)

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.send_message('감사합니다!', ephemeral=True)

