from twitchio.ext import commands
from config import get_bot_config
from modules import *

config = get_bot_config()

class TwitchBot(commands.Bot):
    def __init__(self):
        super().__init__(
            token=config["access_token"],
            prefix=config["prefix"],
            initial_channels=[config["channel"]]
        )
        
        self.access_token = config["access_token"]
        self.client_id = config["client_id"]
        self.channel_name = config["channel"]

    async def event_ready(self):
        print(f"Бот {self.nick} подключен к каналу {config['channel']}")

        # Музыка
        self.add_cog(MusicCommand(self))

        # API — зависимые команды:
        self.add_cog(UptimeCommand(self))
        self.add_cog(FollowageCommand(self))

        # Простые команды:
        self.add_cog(HelloCommand(self))
        self.add_cog(JokeCommand(self))
        self.add_cog(CoinFlipCommand(self))
        self.add_cog(FactCommand(self))
        self.add_cog(HelpCommand(self))
        self.add_cog(BugReportCommand(self))

    async def event_message(self, message):
        if message.echo:
            return
        await self.handle_commands(message)

if __name__ == "__main__":
    bot = TwitchBot()
    bot.run()
