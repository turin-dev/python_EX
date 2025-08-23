import discord

class FruitView(discord.ui.View):
    @discord.ui.select(
        placeholder='과일을 선택하세요',
        options=[
            discord.SelectOption(label='사과', value='apple'),
            discord.SelectOption(label='바나나', value='banana'),
            discord.SelectOption(label='체리', value='cherry'),
        ]
    )
    async def select_callback(self, interaction: discord.Interaction, select: discord.ui.Select):
        await interaction.response.send_message(f'선택한 과일: {select.values[0]}')

