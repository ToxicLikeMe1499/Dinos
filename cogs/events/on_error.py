import nextcord
from nextcord.ext import commands

class on_error_command_not_found(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance (error, commands.CommandNotFound):
            pass
        elif isinstance (error, commands.MessageNotFound):
            pass
        elif isinstance (error, nextcord.errors.NotFound):
            pass
        else:
            pass

def setup(bot):
    bot.add_cog(on_error_command_not_found(bot))