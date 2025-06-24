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
            await ctx.send(f"@{ctx.author.display_name}, шаблон: !заказ <ссылка на Youtube видео>")
            return

        url = parts[1]
        success = self.player.add_to_queue(url, ctx.author.name)

        if success:
            await ctx.send(f"@{ctx.author.display_name}, трек добавлен в очередь.")
        else:
            await ctx.send(f"@{ctx.author.display_name}, не удалось добавить трек.")

    @commands.command(name="скип")
    async def skip(self, ctx: commands.Context):
        user = ctx.author.name
        if not self.player.current_player:
            await ctx.send("Сейчас ничего не играет.")
            return

        is_owner = user == self.bot.channel_name
        is_requester = user == self.player.current_user

        if is_owner or is_requester:
            self.player.skip_requested = True
            await ctx.send("Трек был пропущен.")
        else:
            await ctx.send(f"@{ctx.author.display_name}, пропустить трек может только его заказчик или владелец канала.")

    @commands.command(name="отмена")
    async def cancel(self, ctx: commands.Context):
        result = self.player.cancel_last_request(ctx.author.name)
        if result:
            title = result[1]
            await ctx.send(f'@{ctx.author.display_name}, трек "{title}" удалён из очереди.')
        else:
            await ctx.send(f'@{ctx.author.display_name}, у вас нет треков в очереди.')

    @commands.command(name="трек")
    async def current_track(self, ctx: commands.Context):
        title = self.player.get_current_title()

        if title:
            await ctx.send(f"🎵 Сейчас играет: {title}")
        else:
            await ctx.send("Сейчас ничего не играет.")
