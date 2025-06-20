import os
from twitchio.ext import commands
from dotenv import load_dotenv

load_dotenv()

bot = commands.Bot(
    token = os.getenv("TOKEN"),
    prefix = '!',
    initial_channels = [os.getenv("TARGET_CHANNEL")],
    name = os.getenv("BOT_NAME")
)

@bot.event
async def event_ready():
    print(f'Бот запущен как: {bot.name}')

@bot.command(name = 'hello')
async def hello(ctx):
    await ctx.send(f'Привет, {ctx.author.name}!')

bot.run()