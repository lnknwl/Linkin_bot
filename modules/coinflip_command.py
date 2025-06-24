import random
from twitchio.ext import commands

class CoinFlipCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="монета")
    async def coinflip(self, ctx):
        outcomes = ["Орёл", "Решка", "Ребро"]
        weights = [0.495, 0.495, 0.01]

        result = random.choices(outcomes, weights=weights, k=1)[0]

        if result == "Орёл":
            verb = "выпал"
        elif result == "Решка":
            verb = "выпала"
        else:
            await ctx.send(f"{ctx.author.display_name}, монета приземлилась на ребро! Что за удача?!")
            return

        await ctx.send(f"{ctx.author.display_name}, {verb} {result}!")