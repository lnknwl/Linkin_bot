import aiohttp
import time
from twitchio.ext import commands
from bs4 import BeautifulSoup
from .joke_command import pluralize_seconds

class FactCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.last_fact_time = 0

    @commands.command(name="факт")
    async def fact(self, ctx):
        current_time = time.time()
        elapsed = current_time - self.last_fact_time
        cooldown = 30

        if elapsed < cooldown:
            remaining = int(cooldown - elapsed)
            await ctx.send(f"Следующий факт будет доступен через {pluralize_seconds(remaining)}.")
            return
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get("https://randstuff.ru/fact/ajax/") as resp:
                    if resp.status != 200:
                        print(f"[ОШИБКА] Код {resp.status} при обращении к AJAX-факту")
                        await ctx.send("Не удалось получить факт :(")
                        return

                    html = await resp.text()
                    soup = BeautifulSoup(html, "html.parser")
                    fact_td = soup.find("td")
                    if not fact_td:
                        raise ValueError("Не найден <td> с фактом в AJAX-ответе")

                    fact = fact_td.get_text(strip=True)
                    print(f"[ФАКТ] для пользователя {ctx.author.name}: {fact}")
                    await ctx.send(f"{fact} 🤓")

                    self.last_fact_time = time.time()

        except Exception as e:
            print(f"[ОШИБКА ИСКЛЮЧЕНИЕ] {e}")
            await ctx.send("Произошла ошибка при получении факта :(")