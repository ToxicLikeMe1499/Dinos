import nextcord
from nextcord.ext import commands
from nextcord import FFmpegPCMAudio
import asyncio

class state():
    waiting = 0xFFFF00
    canceled = 0xFF0000
    claimed = 0x00FF00

class VC_SuportCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.playing_audio = False
        self.voice_channel = None
    
    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if before.channel is None and after.channel is not None:
            if after.channel.id == 1249097844242251857 and not member.bot:
                ping = after.channel.guild.get_channel(1249102582371188757)
                role = after.channel.guild.get_role(1222854878422892634)
                test_role = after.channel.guild.get_role(1238883290836897802)
                em = nextcord.Embed(title="Support", description=f"{member.mention} wartet im Support Warteraum", color=state.waiting)
                message = await ping.send(f"{role.mention}{test_role.mention}")
                await message.delete()
                self.message = await ping.send(embed=em)
                if not self.playing_audio:
                    await self.play_audio(after.channel)
            else:
                return
        elif before.channel is not None and after.channel is None:
            if before.channel.id == 1249097844242251857 and not member.bot:
                em = nextcord.Embed(title="Support", description=f"{member.mention} hatte im Support Warteraum vergeblich gewartet", color=state.canceled)
                await self.message.edit(embed=em)
                non_bot_members = [m for m in before.channel.members if not m.bot]
                if len(non_bot_members) == 0 and self.voice_channel:
                    await self.voice_channel.disconnect()
            else:
                return
        else:
            return

    async def play_audio(self, channel):
        try:
            self.playing_audio = True
            self.voice_channel = await channel.connect()
            while True:
                if self.voice_channel and len([m for m in self.voice_channel.channel.members if not m.bot]) > 0:
                    source = FFmpegPCMAudio("assets/support.mp3")  # Use the MP3 file
                    self.voice_channel.play(source, after=lambda e: self.on_audio_finished(e))
                    while self.voice_channel.is_playing():
                        await asyncio.sleep(1)
                    await asyncio.sleep(600)  # Wait for 10 minutes before playing again
                else:
                    await self.voice_channel.disconnect()
                    self.playing_audio = False
                    self.voice_channel = None
                    break
        except Exception as e:
            self.playing_audio = False
            self.voice_channel = None

    def on_audio_finished(self, error):
        if error:
            # Handle the error if needed
            pass
        # No need to set self.playing_audio to False here since we want to keep the loop running

def setup(bot):
    bot.add_cog(VC_SuportCog(bot))
