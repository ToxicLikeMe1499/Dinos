import nextcord
import mysql.connector
from nextcord import Interaction
from nextcord.ext import tasks
from nextcord.ext import commands

class ApplyModal(nextcord.ui.Modal):
    def __init__(self, supporter: bool = False, moderator: bool = False, developer: bool = False, designer: bool = False):
        super().__init__(
            "Bewerbungsformular",
            timeout=1800
        )
        self.role = nextcord.ui.TextInput(
            label="Für welche Rolle bewerben Sie sich?",
            placeholder="Supporter, Moderator, Developer, Designer",
            min_length=8,
            max_length=8,
            required=True
        )
        self.text = nextcord.ui.TextInput(
            label="Warum sollten wir dich nehmen?",
            style=nextcord.TextInputStyle.paragraph,
            min_length=30,
            max_length=500,
            required=True
        )
        self.times = nextcord.ui.TextInput(
            label="In welchen zeiten bist du üblicherweiße online?",
            placeholder="13Uhr - 13:30Uhr",
            max_length=30,
            required=True
        )
        self.infos = nextcord.ui.TextInput(
            label="Sonstige infos?",
            placeholder="Programmiersprachen, Social Media etz.",
            style=nextcord.TextInputStyle.paragraph,
            max_length=500,
            required=False
        )
        self.supporter = supporter
        self.moderator = moderator
        self.developer = developer
        self.designer = designer
        self.add_item(self.role)
        self.add_item(self.text)
        self.add_item(self.times)
        self.add_item(self.infos)
        self.add_item(self.supporter)
        self.add_item(self.moderator)
        self.add_item(self.developer)
        self.add_item(self.designer)
    async def callback(self, interaction: Interaction):
        self.role.value = self.role.value.lower()
        if self.role.value == "supporter":
            if self.supporter == True:
                possible = True
            else:
                possible = False
        if self.role.value == "moderator":
            if self.moderator == True:
                possible = True
            else:
                possible = False
        if self.role.value == "developer":
            if self.developer == True:
                possible = True
            else:
                possible = False
        if self.role.value == "designer":
            if self.designer == True:
                possible = True
            else:
                possible = False
        else:
            await interaction.response.send_message("Du hast eine ungültige option eingegeben", ephemeral=True)
        if possible == True:
            em = nextcord.Embed(title="Erfolgreich", description="Deine bewerbung wurde erfolgreich eingereicht", color=nextcord.Color.green())
        else:
            em = nextcord.Embed(title="Fehler", description="Diese stelle sucht keine neuzugänge", color=nextcord.Color.red)
        await interaction.response.send_message(embed=em, ephemeral=True)

class ApplyView(nextcord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
    
    @nextcord.ui.button(label="Bewerbung einrechen", style=nextcord.ButtonStyle.green, custom_id="ApllyView:green")
    async def apply_button(self, button:nextcord.ui.Button, interaction: Interaction):
        self.DB = mysql.connector.connect(
            host="161.97.76.124",
            port=3306,
            user="u138_gx5qKWntiH",
            password="XD13F=Av60OPhh2Y.Fq@5F9k",
            database="s138_dino"
        )
        self.Cursor = self.DB.cursor()
        self.Cursor.execute("SELECT state FROM apply_state WHERE role = Dinoporter")
        dinoporter_state = self.Cursor.fetchone()
        self.Cursor.execute("SELECT state FROM apply_state WHERE role = Dinorator")
        dinorator_state = self.Cursor.fetchone()
        self.Cursor.execute("SELECT state FROM apply_state WHERE role = Developer")
        developer_state = self.Cursor.fetchone()
        self.Cursor.execute("SELECT state FROM apply_state WHERE role = Designer")
        designer_state = self.Cursor.fetchone()
        if dinoporter_state == 1:
            dinoporter_state=True
        else:
            dinoporter_state=False
        await interaction.response.send_modal(ApplyModal(supporter=dinoporter_state))

class ApplyCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.apply.start()

    @commands.Cog.listener()
    async def on_ready(self):
        self.bot.add_view(ApplyView())

    @tasks.loop(minutes=15)
    async def apply(self):
        await self.bot.wait_until_ready()
        self.DB = mysql.connector.connect(
            host="161.97.76.124",
            port=3306,
            user="u138_gx5qKWntiH",
            password="XD13F=Av60OPhh2Y.Fq@5F9k",
            database="s138_dino"
        )
        self.Cursor = self.DB.cursor()
        self.Cursor.execute("SELECT apply_channel FROM data")
        self.apply_guild = self.bot.get_guild(1217146612472610928)
        self.apply_channel = self.apply_guild.get_channel(self.Cursor.fetchone())
        self.Cursor.execute("SELECT apply_message FROM data")
        self.message = self.apply_channel.fetch_message(self.Cursor.fetchone())
        self.Cursor.execute("SELECT state FROM apply_state WHERE role = Dinoporter")
        dinoporter_state = self.Cursor.fetchone()
        self.Cursor.execute("SELECT state FROM apply_state WHERE role = Dinorator")
        dinorator_state = self.Cursor.fetchone()
        self.Cursor.execute("SELECT state FROM apply_state WHERE role = Developer")
        developer_state = self.Cursor.fetchone()
        self.Cursor.execute("SELECT state FROM apply_state WHERE role = Designer")
        designer_state = self.Cursor.fetchone()
        self.Cursor.close()
        self.DB.close()
        em = nextcord.Embed(title="Bewerben", description="Du willst ein teil von unserem wundervollen team werden?\nDann drück einfach unten auf den knopf `Bewerbung einrechen` und fülle das formular aus.\nUnten siehst du die verfügbaren stellen\nbei rückfragen werden wir uns bei dir melden.\n\nLG: Das Dino Team")
        if dinoporter_state[0] == 1:
            em.add_field(name=":green_circle: Supporter", value="Supporter Bewerbungen sind zurzeit offen", inline=False)
        else:
            em.add_field(name=":red_circle: Supporter", value="Supporter Bewerbungen sind zurzeit geschlossen", inline=False)
        if dinorator_state[0] == 1:
            em.add_field(name=":green_circle: Moderator", value="Moderator Bewerbungen sind zurzeit offen", inline=False)
        else:
            em.add_field(name=":red_circle: Moderator", value="Moderator Bewerbungen sind zurzeit geschlossen", inline=False)
        if developer_state[0] == 1:
            em.add_field(name=":green_circle: Developer", value="Developer Bewerbungen sind zurzeit offen", inline=False)
        else:
            em.add_field(name=":red_circle: Developer", value="Developer Bewerbungen sind zurzeit geschlossen", inline=False)
        if designer_state[0] == 1:
            em.add_field(name=":green_circle: Designer", value="Designer Bewerbungen sind zurzeit offen", inline=False)
        else:
            em.add_field(name=":red_circle: Designer", value="Designer Bewerbungen sind zurzeit geschlossen", inline=False)
        em.set_author(icon_url=self.message.guild.icon.url, name=self.message.guild.name)
        await self.message.edit(embed=em, view=ApplyView())

    @commands.command()
    async def apply_message(self, ctx):
        self.DB = mysql.connector.connect(
            host="161.97.76.124",
            port=3306,
            user="u138_gx5qKWntiH",
            password="XD13F=Av60OPhh2Y.Fq@5F9k",
            database="s138_dino"
        )
        self.Cursor = self.DB.cursor()
        self.Cursor.execute("SELECT state FROM apply_state WHERE role = 'Dinoporter'")
        dinoporter_state = self.Cursor.fetchone()
        self.Cursor.execute("SELECT state FROM apply_state WHERE role = 'Dinorator'")
        dinorator_state = self.Cursor.fetchone()
        self.Cursor.execute("SELECT state FROM apply_state WHERE role = 'Developer'")
        developer_state = self.Cursor.fetchone()
        self.Cursor.execute("SELECT state FROM apply_state WHERE role = 'Designer'")
        designer_state = self.Cursor.fetchone()
        self.Cursor.close()
        self.DB.close()
        em = nextcord.Embed(title="Bewerben", description="Du willst ein teil von unserem wundervollen team werden?\nDann drück einfach unten auf den knopf `Bewerbung einrechen` und fülle das formular aus.\nUnten siehst du die verfügbaren stellen\nbei rückfragen werden wir uns bei dir melden.\n\nLG: Das Dino Team")
        if dinoporter_state[0] == 1:
            em.add_field(name=":green_circle: Supporter", value="Supporter Bewerbungen sind zurzeit offen", inline=False)
        else:
            em.add_field(name=":red_circle: Supporter", value="Supporter Bewerbungen sind zurzeit geschlossen", inline=False)
        if dinorator_state[0] == 1:
            em.add_field(name=":green_circle: Moderator", value="Moderator Bewerbungen sind zurzeit offen", inline=False)
        else:
            em.add_field(name=":red_circle: Moderator", value="Moderator Bewerbungen sind zurzeit geschlossen", inline=False)
        if developer_state[0] == 1:
            em.add_field(name=":green_circle: Developer", value="Developer Bewerbungen sind zurzeit offen", inline=False)
        else:
            em.add_field(name=":red_circle: Developer", value="Developer Bewerbungen sind zurzeit geschlossen", inline=False)
        if designer_state[0] == 1:
            em.add_field(name=":green_circle: Designer", value="Designer Bewerbungen sind zurzeit offen", inline=False)
        else:
            em.add_field(name=":red_circle: Designer", value="Designer Bewerbungen sind zurzeit geschlossen", inline=False)
        em.set_author(icon_url=ctx.guild.icon.url, name=ctx.guild.name)

def setup(bot):
    bot.add_cog(ApplyCog(bot))