import os
from dotenv import load_dotenv
from twitchio.ext import commands
from token_utils import refresh_access_token

load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
refresh_token = os.getenv("REFRESH_TOKEN")

access_token, _ = refresh_access_token(client_id, client_secret, refresh_token)

bot = commands.Bot(
    token=access_token,
    prefix=os.getenv("PREFIX"),
    initial_channels=[os.getenv("TARGET_CHANNEL")]
)

@bot.event
async def event_ready():
    print(f"🤖 Бот {bot.nick} подключен к каналу {os.getenv('TARGET_CHANNEL')}")

@bot.command(name="hello")
async def hello(ctx):
    await ctx.send(f"Привет, {ctx.author.name}!")

bot.run()