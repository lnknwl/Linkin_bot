import aiohttp
import datetime
from twitchio.ext import commands
from .base_api_cog import BaseTwitchApiCog

class FollowageCommand(BaseTwitchApiCog):
    def __init__(self, bot):
        super().__init__(bot)

    def _format_follow_duration(self, delta: datetime.timedelta) -> str:
        days = delta.days
        years, rem = divmod(days, 365)
        months, days = divmod(rem, 30)

        def _russian_word(n, one, few, many):
            if 11 <= n % 100 <= 14:
                return many
            if n % 10 == 1:
                return one
            if 2 <= n % 10 <= 4:
                return few
            return many

        parts = []
        if years:
            parts.append(f"{years} {_russian_word(years, 'год', 'года', 'лет')}")
        if months:
            parts.append(f"{months} {_russian_word(months, 'месяц', 'месяца', 'месяцев')}")
        if days:
            parts.append(f"{days} {_russian_word(days, 'день', 'дня', 'дней')}")

        return " ".join(parts) if parts else "меньше дня"

    @commands.command(name="followage")
    async def followage(self, ctx: commands.Context):
        headers = {
            "Authorization": self.access_token,
            "Client-Id": self.client_id
        }

        async with aiohttp.ClientSession() as session:
            async def get_user_id(login: str) -> str:
                resp = await session.get(f"https://api.twitch.tv/helix/users?login={login}", headers=headers)
                json = await resp.json()
                return json["data"][0]["id"]

            user_id = await get_user_id(ctx.author.name)
            channel_id = await get_user_id(self.channel_name)

            resp = await session.get(
                f"https://api.twitch.tv/helix/channels/followers?broadcaster_id={channel_id}&user_id={user_id}",
                headers=headers
            )
            data = await resp.json()

            if data.get("total", 0) == 0 or not data.get("data"):
                await ctx.send(f"@{ctx.author.name}, вы не отслеживаете канал.")
                return

            followed_at = data["data"][0]["followed_at"]
            follow_date = datetime.datetime.fromisoformat(followed_at.replace("Z", "+00:00"))
            delta = datetime.datetime.now(datetime.timezone.utc) - follow_date

            duration = self._format_follow_duration(delta)
            await ctx.send(f"@{ctx.author.name}, вы отслеживаете канал уже {duration}.")

