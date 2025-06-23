from twitchio.ext import commands

class HelpCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="команды")
    async def commands_list(self, ctx):
        prefix = "!"
        cmds = [
            f"{prefix}{cmd.name}"
            for cmd in self.bot.commands.values()
            if getattr(cmd, "hidden", False) is False and cmd.name != "команды"
        ]
        await ctx.send("Доступные команды: " + ", ".join(cmds))

