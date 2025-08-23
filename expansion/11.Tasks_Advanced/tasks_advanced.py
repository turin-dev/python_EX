from discord.ext import tasks, commands
import asyncio

class MyCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.data = []
        self.lock = asyncio.Lock()
        self.bulker.start()

    @tasks.loop(seconds=10.0)
    async def bulker(self):
        async with self.lock:
            # 데이터 일괄 처리
            print('bulk update')

    @bulker.after_loop
    async def after_bulker(self):
        print('루프 종료')

