import random
import aiohttp
from bs4 import BeautifulSoup
from twitchio.ext import commands
import re
import time

def pluralize_seconds(n):
    n = int(n)
    if 11 <= (n % 100) <= 14:
        return f"{n} секунд"
    elif n % 10 == 1:
        return f"{n} секунда"
    elif 2 <= n % 10 <= 4:
        return f"{n} секунды"
    else:
        return f"{n} секунд"

class CommandModule(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.last_joke_time = 0

    @commands.command(name="hello")
    async def hello(self, ctx):
        responses = [
            f"Привет, {ctx.author.name}!",
            f"Дарова, {ctx.author.name}!",
            f"О, {ctx.author.name}! Рад тебя видеть!"
        ]
        response = random.choice(responses)
        await ctx.send(response)

    @commands.command(name="анекдот")
    async def joke(self, ctx):
        current_time = time.time()
        remain = current_time - self.last_joke_time
        remaining = int(90 - remain)
        if remain < 90:
            await ctx.send(f"Следующий анекдот будет доступен через {pluralize_seconds(remaining)}.")
            return

        url = "https://baneks.ru/random"

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status != 200:
                    await ctx.send("Ошибка при получении анекдота :(")
                    return
                html = await response.text()

        soup = BeautifulSoup(html, "html.parser")
        article = soup.find("article")

        if not article:
            await ctx.send("Анекдот не найден :(")
            return

        h2 = article.find("h2")
        joke_id = None
        if h2:
            match = re.search(r"#(\d+)", h2.text)
            if match:
                joke_id = match.group(1)

        p = article.find("p")
        if not p:
            await ctx.send("Анекдот пустой :(")
            return

        for br in p.find_all("br"):
            previous = br.previous_sibling
            if previous and isinstance(previous, str):
                br.insert_before(" ")

        joke = p.get_text(strip=True)

        if len(joke) > 450:
            joke = joke[:447] + "..."

        await ctx.send(joke)

        self.last_joke_time = time.time()

        if joke_id:
            print(f"[АНЕКДОТ #{joke_id}] отправлен пользователю {ctx.author.name}")
        else:
            print(f"[АНЕКДОТ без номера] отправлен пользователю {ctx.author.name}")