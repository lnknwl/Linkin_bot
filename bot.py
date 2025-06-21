from twitchio.ext import commands
from config import get_bot_config
from modules.commands import CommandModule
from modules.joke_command import JokeCommand

config = get_bot_config()

class TwitchBot(commands.Bot):
    def __init__(self):
        super().__init__(
            token=config["access_token"],
            prefix=config["prefix"],
            initial_channels=[config["channel"]]
        )

    async def event_ready(self):
        print(f"Бот {self.nick} подключен к каналу {config['channel']}")
        self.add_cog(CommandModule(self))
        self.add_cog(JokeCommand(self))

    async def event_message(self, message):
        if message.echo:
            return
        await self.handle_commands(message)

if __name__ == "__main__":
    bot = TwitchBot()
    bot.run()
