import nextcord
from nextcord import Interaction
from nextcord.ext import commands

class RegelnView(nextcord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
    
    @nextcord.ui.button(label="Akzeptieren", style=nextcord.ButtonStyle.success, custom_id="rules_accept")
    async def accept(self, button: nextcord.ui.Button, interaction: Interaction):
        role = interaction.guild.get_role(1238789598361157683)
        if interaction.user.get_role(role.id):
            await interaction.response.send_message("Du hast bereits die Regeln akzeptiert!", ephemeral=True)
        else:
            await interaction.user.add_roles(role)
            await interaction.response.send_message("Du hast die Regeln akzeptiert!", ephemeral=True, delete_after=30)

class EmbedCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        self.bot.add_view(RegelnView())

    @nextcord.slash_command(name="embed", description="keine funktion", default_member_permissions=nextcord.Permissions(manage_messages=True), guild_ids=[1180167998342975578, 1217146612472610928])
    async def embed(self, interaction: Interaction):
        pass

    @embed.subcommand(name="senden", description="sendet ein Embed")
    async def send(
        self,
        interaction: Interaction,
        embed = nextcord.SlashOption(
            name="embed",
            description="Welches embed soll gesendet werden",
            required=True,
            choices=["Regeln", "CL5"]
        )
    ):
        if embed == "Regeln":
            em = nextcord.Embed(title="Regelwerk Discord", description="Hier ist eine kleine übersicht zu unseren Discord Regeln.", color=nextcord.Color.dark_theme())
            em.add_field(name="Regel 1", value="Du musst 13 Jahre oder älter sein, um in unserem Clan zu sein. Dies ist eine Regel der ToS von Discord. Wenn du gegen diese Regel verstößt, wirst du dauerhaft gebannt.", inline=False)
            em.add_field(name="Regel 2", value="Ein freundlicher und respektvoller Umgang mit User und Team ist Pflicht.", inline=False)
            em.add_field(name="Regel 3", value="NSFW-Inhalte wie Pornographie ist bei uns verboten.", inline=False)
            em.add_field(name="Regel 4", value="Störgeräusche in einem VC sind verboten. Bitte nutzt Push-To-Talk bie so einen fall", inline=False)
            em.add_field(name="Regel 5", value="Werbung in DM und auf Server ist verboten und wird mit einem Ban bestraft.", inline=False)
            em.add_field(name="Regel 6", value="Das Befolgen der [Discord-Nutzungsbedingungen (ToS)](https://discord.com/terms) und den [Community-Richtlinien (Guidelines)](https://discord.com/guidelines) ist Pflicht.", inline=False)
            em.add_field(name="Regel 7", value="Wenn du in einem Sprachchannel Audio oder Screen aufnimmst, muss jeder im Raum damit einverstanden sein.", inline=False)
            em.add_field(name="Regel 8", value="Rassistische und Nazistische Inhalte sind verboten.", inline=False)
            em.add_field(name="Regel 9", value="Spamming ist verboten", inline=False)
            em.add_field(name="Regel 10", value="Allgemein gilt, das Team hat Recht bei anweißungen ist diesem Folge zu leisten", inline=False)
            em.add_field(name="Regel 11", value="Identitätsdiebstahl ist verboten.", inline=False)
            em.add_field(name="Regel 12", value="Reflinks sind verboten.", inline=False)
            em.add_field(name="Regel 13", value="Es ist verboten alles über <@&1238117313656651858> ohne Grund zu pingen.", inline=False)
            em.add_field(name="Regel 14", value="Die Regel 7 trit auser Kraft, wenn man Beiweiße aufnimmt", inline=False)
            em.add_field(name="Regel 15", value="Im <#1222502199326933084> sind gif's verboten sowas in <#1222502803000262688>", inline=False)
            await interaction.response.send_message(embed=em, view=RegelnView())
        elif embed == "CL5":
            em = nextcord.Embed(title="Create Live 5 Partnerschaft", description="Herzlich willkommen zu der Partnerschaft von Gleisi's Bahnhofsgemeinschaft!\n Du suchst einen guten Create Live 5 Server?\nDann ist du hier richtig.\nWir beiten dir eine freundliche Community und viele Möglichkeiten an.\n Alle infos findest du unten bei den Knöpfen", color=nextcord.Color.dark_theme())
            view=nextcord.ui.View()
            style=nextcord.ButtonStyle.grey
            item = nextcord.ui.Button(style=style, label="TikTok", url="https://www.tiktok.com/@itsgleisi")
            view.add_item(item)
            style=nextcord.ButtonStyle.blurple
            item = nextcord.ui.Button(style=style, label="Discord", url="https://discord.gg/pEtaVpFHfU")
            view.add_item(item)
            await interaction.response.send_message(embed=em, view=view)

def setup(bot):
    bot.add_cog(EmbedCog(bot))