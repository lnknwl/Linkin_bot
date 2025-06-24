import random
from twitchio.ext import commands

class HelloCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="hello")
    async def hello(self, ctx):
        responses = [
            f"Привет, {ctx.author.display_name}!",
            f"Дарова, {ctx.author.display_name}!",
            f"О, {ctx.author.display_name}! Рад тебя видеть!"
        ]
        response = random.choice(responses)
        await ctx.send(response)