import random
from twitchio.ext import commands

class CommandModule(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="hello")
    async def hello(self, ctx):
        responses = [
            f"Привет, {ctx.author.name}!",
            f"Дарова, {ctx.author.name}!",
            f"О, {ctx.author.name}! Рад тебя видеть!"
        ]
        response = random.choice(responses)
        await ctx.send(response)