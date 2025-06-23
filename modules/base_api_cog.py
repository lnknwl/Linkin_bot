from twitchio.ext import commands

class BaseTwitchApiCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.access_token = f"Bearer {bot.access_token}"
        self.client_id = bot.client_id
        self.channel_name = bot.channel_name
        self.channel_id = None