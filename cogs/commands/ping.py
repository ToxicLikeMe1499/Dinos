import time
import nextcord
from nextcord import Interaction
from nextcord.ext import commands

class ping(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx):
        if round(self.bot.latency * 1000) <= 50:
            embed=nextcord.Embed(title="PING", description=f":ping_pong: Pingpingpingpingping! Der ping ist **{round(self.bot.latency *1000)}** ms!", color=0x44ff44)
        elif round(self.bot.latency * 1000) <= 100:
            embed=nextcord.Embed(title="PING", description=f":ping_pong: Pingpingpingpingping! Der ping ist **{round(self.bot.latency *1000)}** ms!", color=0xffd000)
        elif round(self.bot.latency * 1000) <= 200:
            embed=nextcord.Embed(title="PING", description=f":ping_pong: Pingpingpingpingping! Der ping ist **{round(self.bot.latency *1000)}** ms!", color=0xff6600)
        else:
            embed=nextcord.Embed(title="PING", description=f":ping_pong: Pingpingpingpingping! Der ping ist **{round(self.bot.latency *1000)}** ms!", color=0x990000)
        await ctx.message.delete()
        await ctx.send(embed=embed, delete_after=30)
    
    @nextcord.slash_command(name="ping", guild_ids=[1180167998342975578, 1217146612472610928])
    async def s_ping(self, interaction: Interaction):
        if round(self.bot.latency * 1000) <= 50:
            embed=nextcord.Embed(title="PING", description=f":ping_pong: Pingpingpingpingping! Der ping ist **{round(self.bot.latency *1000)}** ms!", color=0x44ff44)
        elif round(self.bot.latency * 1000) <= 100:
            embed=nextcord.Embed(title="PING", description=f":ping_pong: Pingpingpingpingping! Der ping ist **{round(self.bot.latency *1000)}** ms!", color=0xffd000)
        elif round(self.bot.latency * 1000) <= 200:
            embed=nextcord.Embed(title="PING", description=f":ping_pong: Pingpingpingpingping! Der ping ist **{round(self.bot.latency *1000)}** ms!", color=0xff6600)
        else:
            embed=nextcord.Embed(title="PING", description=f":ping_pong: Pingpingpingpingping! Der ping ist **{round(self.bot.latency *1000)}** ms!", color=0x990000)
        await interaction.send(embed=embed, delete_after=30)

def setup(bot):
    bot.add_cog(ping(bot))