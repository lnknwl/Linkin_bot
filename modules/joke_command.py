import aiohttp
from bs4 import BeautifulSoup
from twitchio.ext import commands
import re
import time
import os

def pluralize_seconds(n):
    n = int(n)
    if 11 <= (n % 100) <= 14:
        return f"{n} секунд"
    elif n % 10 == 1:
        return f"{n} секунду"
    elif 2 <= n % 10 <= 4:
        return f"{n} секунды"
    else:
        return f"{n} секунд"
    
def load_banwords(filename="banwords.txt"):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    full_path = os.path.join(base_dir, filename)

    with open(full_path, "r", encoding="utf-8") as f:
        return set(word.strip().lower() for word in f if word.strip())

class JokeCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.last_joke_time = 0
        self.banwords = load_banwords()

    @commands.command(name="анекдот")
    async def joke(self, ctx):
        current_time = time.time()
        remain = current_time - self.last_joke_time
        
        if remain < 60:
            remaining = int(60 - remain)
            await ctx.send(f"Следующий анекдот будет доступен через {pluralize_seconds(remaining)}.")
            return

        url = "https://baneks.ru/random"

        joke = ""
        joke_id = None

        async with aiohttp.ClientSession() as session:
            while True:
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
                if h2:
                    match = re.search(r"#(\d+)", h2.text)
                    if match:
                        joke_id = match.group(1)

                p = article.find("p")
                if not p:
                    await ctx.send("Анекдот пустой :(")
                    return

                joke = " ".join(p.stripped_strings)

                if any(word in joke.lower() for word in self.banwords):
                    print(f"[БАНВОРД] анекдот #{joke_id or '?'} отклонён")
                    continue

                if len(joke) > 500:
                    print(f"[ДЛИНА >500] анекдот #{joke_id or '?'} ({len(joke)} символов) пропущен")
                    continue

                break

        await ctx.send(joke)
        self.last_joke_time = time.time()

        if joke_id:
            print(f"[АНЕКДОТ #{joke_id}] отправлен пользователю {ctx.author.name}")
        else:
            print(f"[АНЕКДОТ без номера] отправлен пользователю {ctx.author.name}")