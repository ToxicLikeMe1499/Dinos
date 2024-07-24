from datetime import datetime
from nextcord.ext import commands
from assets.config import F, S

def get_time():
    now = datetime.now()
    dt_string = now.strftime("%Y-%m-%d %H:%M:%S")
    return dt_string

def load_curse_words(file_path):
    with open(file_path, "r") as file:
        curse_words = file.read().splitlines()
    return curse_words

class messageCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.curse_words = load_curse_words("assets/curse.txt")

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        elif message.channel.name.startswith("ticket"):
            pass
        else:
            # Check if the message contains any curse words
            if any(curse_word in message.content.lower() for curse_word in self.curse_words):
                await message.delete()
            else:
                print(F.y + S.D + "[" + get_time() + "] " + F.b + S.N + message.channel.name + F.R_ALL + " | " + message.author.name + ": " + message.content)

def setup(bot):
    bot.add_cog(messageCog(bot))
