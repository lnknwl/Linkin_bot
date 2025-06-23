import aiohttp
from datetime import datetime, timezone
from twitchio.ext import commands
from .base_api_cog import BaseTwitchApiCog

class UptimeCommand(BaseTwitchApiCog):
    def __init__(self, bot):
        super().__init__(bot)

    async def get_stream_data(self):
        url = "https://api.twitch.tv/helix/streams"
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Client-Id": self.client_id
        }
        params = {"user_login": self.channel_name}

        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers, params=params) as resp:
                if resp.status != 200:
                    return None
                return await resp.json()
            
    def _format_duration(self, hours: int, minutes: int) -> str:
        def _russian_word(n, one, few, many):
            if 11 <= n % 100 <= 14:
                return many
            if n % 10 == 1:
                return one
            if 2 <= n % 10 <= 4:
                return few
            return many

        parts = []
        if hours > 0:
            parts.append(f"{hours} {_russian_word(hours, 'час', 'часа', 'часов')}")
        if minutes > 0 or hours == 0:
            parts.append(f"{minutes} {_russian_word(minutes, 'минуту', 'минуты', 'минут')}")
        return " ".join(parts)

    @commands.command(name="uptime")
    async def stream_time(self, ctx):
        data = await self.get_stream_data()

        if not data or not data.get("data"):
            await ctx.send("Стрим сейчас оффлайн.")
            return

        started_at_str = data["data"][0]["started_at"]

        started_at = datetime.strptime(started_at_str, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)

        now = datetime.now(timezone.utc)

        delta = now - started_at

        hours, remainder = divmod(int(delta.total_seconds()), 3600)
        minutes = remainder // 60

        duration_str = self._format_duration(hours, minutes)
        await ctx.send(f"Стрим идёт уже {duration_str}.")