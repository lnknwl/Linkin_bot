import aiohttp
from twitchio.ext import commands

class FactCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="факт")
    async def fact(self, ctx):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get("https://uselessfacts.jsph.pl/api/v2/facts/random?language=en") as resp:
                    if resp.status != 200:
                        print(f"[ОШИБКА] Не удалось получить факт (код {resp.status})")
                        await ctx.send("Не удалось получить факт :(")
                        return
                    data = await resp.json()
                    fact = data["text"]
                    print(f"[ФАКТ] для пользователя {ctx.author.name}: {fact}")
                    await ctx.send(fact)

        except Exception as e:
            print(f"[ОШИБКА ИСКЛЮЧЕНИЕ] {e}")
            await ctx.send("Произошла ошибка при получении факта :(")