import json
import os
from twitchio.ext import commands
from datetime import datetime

class BugReportCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bug_file_path = os.path.join(os.path.dirname(__file__), "..", "logs", "bugs.json")
        os.makedirs(os.path.dirname(self.bug_file_path), exist_ok=True)
        if not os.path.exists(self.bug_file_path):
            with open(self.bug_file_path, "w", encoding="utf-8") as f:
                json.dump([], f, ensure_ascii=False, indent=2)
    
    def save_bug(self, user, message):
        with open(self.bug_file_path, "r+", encoding="utf-8") as f:
            data = json.load(f)
            data.append({
                "user": user,
                "message": message,
                "timestamp": datetime.now().strftime("%H:%M %d-%m-%Y")
            })
            f.seek(0)
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    @commands.command(name="баг")
    async def bug(self, ctx):
        message = ctx.message.content[len("!баг"):].strip()
        if not message:
            await ctx.send(f"{ctx.author.display_name}, нужно указать описание проблемы (!баг <проблема>).")
            return

        self.save_bug(ctx.author.name, message)
        await ctx.send(f"{ctx.author.display_name}, спасибо! Проблема записана.")