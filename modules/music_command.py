from twitchio.ext import commands
from music.music_player import MusicPlayer

class MusicCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.player = MusicPlayer()

    @commands.command(name="заказ")
    async def music(self, ctx: commands.Context):
        parts = ctx.message.content.split(" ", 1)
        if len(parts) < 2:
            await ctx.send(f"@{ctx.author.name}, шаблон: !заказ <ссылка на Youtube видео>")
            return

        url = parts[1]
        success = self.player.add_to_queue(url, ctx.author.name)

        if success:
            await ctx.send(f"@{ctx.author.name}, трек добавлен в очередь.")
        else:
            await ctx.send(f"@{ctx.author.name}, не удалось добавить трек.")


