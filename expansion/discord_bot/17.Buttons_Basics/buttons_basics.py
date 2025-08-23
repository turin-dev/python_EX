import discord

class MyView(discord.ui.View):
    @discord.ui.button(label='눌러 보세요', style=discord.ButtonStyle.primary)
    async def click_me(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message('버튼이 클릭되었습니다!')

@bot.command()
async def button(ctx):
    await ctx.send('이 버튼을 클릭하세요.', view=MyView())

