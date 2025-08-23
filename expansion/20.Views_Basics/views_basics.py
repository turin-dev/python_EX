import discord

class SimpleView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=30)
        self.add_item(discord.ui.Button(label='확인', style=discord.ButtonStyle.success))

@bot.command()
async def show_view(ctx):
    await ctx.send('이건 뷰 예제입니다.', view=SimpleView())

