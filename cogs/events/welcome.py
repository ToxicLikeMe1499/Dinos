import nextcord
import random
from nextcord.ext import commands
from nextcord import Interaction

class welcome(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.list_description = ["Hi wie geht es dir?\nGut hoffen wir.\nstell dich doch gerne mal vor oder sag einfach nur hi <#1222502199326933084>\ndu willst auf unsere server? dann whiteliste dich doch gerne hier <#1234203030233022524>", 'Hallo!\nAlles klar bei dir?\nWenn du Lust hast, kannst du dich gerne vorstellen oder einfach nur "Hi" sagen in <#1222502199326933084>.\nUnd wenn du unseren Minecraft-Server beitreten möchtest, vergiss nicht, dich auf der Whitelist einzutragen: <#1234203030233022524>.\n\nWir freuen uns darauf, dich dort zu sehen! 🎮']

    @commands.Cog.listener()
    async def on_member_join(self, member):
        ch_welcome = self.bot.get_channel(1229784315039187036)
        em = nextcord.Embed(
            title=f"Willkommen bei den {member.guild.name} {member.name}",
            description=random.choice(self.list_description),
            color=0x5865F2,
            )
        em.set_footer(text="Liebe Grüße Die Dinos | Der Server mit den besten Events")
        em.set_author(
            name="Die Dinos",
            icon_url=f"{member.guild.icon.url}"
            )
        await ch_welcome.send(embed=em)

def setup(bot):
    bot.add_cog(welcome(bot))