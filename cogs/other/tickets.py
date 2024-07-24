import nextcord
import mysql.connector
from nextcord import Interaction
from nextcord.ext import commands

class AddUser(nextcord.ui.Modal):
    def __init__(self, channel):
        super().__init__("Nutzer Hinzufügen", timeout=300)
        self.channel = channel

        self.user = nextcord.ui.TextInput(
            label="Nutzer ID",
            min_length=2,
            max_length=30,
            required=True,
            placeholder="123456789"
        )
        self.add_item(self.user)
    
    async def callback(self, interaction: Interaction):
        user = interaction.guild.get_member(int(self.user.value))
        if user is None:
            em = nextcord.Embed(
                title="Fehlgechlagen!",
                description=f"Der Nutzer mit der id `{int(self.user.value)}` wurde nicht gefunden!\nStelle sicher, dass der Nutzer im Server ist oder lade ihn ein!",
                color=nextcord.Color.red()
            )
            return await interaction.send(embed=em, delete_after=30)
        overwrite = nextcord.PermissionOverwrite(
            read_message_history=True,
            read_messages=True,
            send_messages=True,
            add_reactions=True
        )
        await self.channel.set_permissions(user, overwrite=overwrite)
        em = nextcord.Embed(
            title="Erfolgreich!",
            description=f"Der Nutzer {user.mention} wurde hinzugefügt!",
            color=nextcord.Color.green()
        )
        await interaction.send(embed=em)

class RemoveUser(nextcord.ui.Modal):
    def __init__(self, channel):
        super().__init__("Nutzer Entfernen", timeout=300)
        self.channel = channel

        self.user = nextcord.ui.TextInput(
            label="Nutzer ID",
            min_length=2,
            max_length=30,
            required=True,
            placeholder="123456789"
        )
        self.add_item(self.user)
    
    async def callback(self, interaction: Interaction):
        user = interaction.guild.get_member(int(self.user.value))
        if user is None:
            em = nextcord.Embed(
                title="Fehlgechlagen!",
                description=f"Der Nutzer mit der id `{int(self.user.value)}` wurde nicht gefunden!",
                color=nextcord.Color.red()
            )
            return await interaction.send(embed=em, delete_after=30)
        overwrite = nextcord.PermissionOverwrite(
            read_message_history=False,
            read_messages=False,
            send_messages=False,
            add_reactions=False
        )
        await self.channel.set_permissions(user, overwrite=overwrite)
        em = nextcord.Embed(
            title="Erfolgreich!",
            description=f"Der Nutzer {user.mention} wurde entfernt!",
            color=nextcord.Color.green()
        )
        await interaction.send(embed=em)

class CreateTicket(nextcord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
    
    @nextcord.ui.button(label="Erstelle ein Ticket", style=nextcord.ButtonStyle.blurple, custom_id="create_ticket:blurple")
    async def create_ticket(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.DB = mysql.connector.connect(
            host="161.97.76.124",
            port=3306,
            user="u138_gx5qKWntiH",
            password="XD13F=Av60OPhh2Y.Fq@5F9k",
            database="s138_dino"
        )
        self.Cursor = self.DB.cursor()
        
        self.Cursor.execute("SELECT COUNT(*) FROM tickets WHERE creator = %s AND closed = 0", (interaction.user.id,))
        open_tickets_count = self.Cursor.fetchone()[0]
        
        if open_tickets_count >= 2:
            em = nextcord.Embed(title="Fehler", description="Du hast bereits 2 geöffnete tickets!")
            await interaction.response.send_message(embed=em, ephemeral=True)
            self.Cursor.close()
            self.DB.close()
            return
        
        self.Cursor.execute("SELECT MAX(id) + 1 FROM tickets")
        ticket_id = self.Cursor.fetchone()[0]
        overwrites = {
            interaction.guild.default_role: nextcord.PermissionOverwrite(read_messages=False),
            interaction.guild.me: nextcord.PermissionOverwrite(read_messages=True, read_message_history=True, send_messages=True, add_reactions=True),
            interaction.user: nextcord.PermissionOverwrite(read_messages=True, read_message_history=True, send_messages=True, add_reactions=True),

            interaction.guild.get_role(1222854878422892634): nextcord.PermissionOverwrite(read_messages=True, read_message_history=True, send_messages=True, add_reactions=True, manage_messages=True),
            interaction.guild.get_role(1222854418710528101): nextcord.PermissionOverwrite(read_messages=True, read_message_history=True, send_messages=True, add_reactions=True, manage_messages=True),
            interaction.guild.get_role(1231237145902059591): nextcord.PermissionOverwrite(read_messages=True, read_message_history=True, send_messages=True, add_reactions=True, manage_messages=True)
        }
        member = interaction.user
        category = interaction.guild.get_channel(1222855543236853841)
        channel = await interaction.guild.create_text_channel(name=f"ticket-{ticket_id}", category=category, overwrites=overwrites)
        await interaction.response.send_message(f"Ein Ticket wurde erstellt: {channel.mention} {member.mention}", ephemeral=True)
        em = nextcord.Embed(
            title="Willkommen im Support",
            description=(
                f"> Willkommen im Support von {interaction.guild.name}.\n"
                "> Ein Teamler wird in Kürze bei dir sein.\n"
                "> Beschreibe einfach dein Anliegen schon mal, damit wir dir so schnell wie möglich helfen können.\n"
                "> Wenn dies ein Versehen war, schließe einfach das Ticket wieder.\n"
                "> Wir kümmern uns so schnell wie möglich um dich.\n\n"
                "LG: Das Dino Team"
            ),
            color=0x5865F2
        )
        r1 = interaction.guild.get_role(1231237145902059591)
        r2 = interaction.guild.get_role(1222854878422892634)
        r3 = interaction.guild.get_role(1222854418710528101)
        await channel.send(f"{interaction.user.mention}", embed=em, view=TicketSettings())
        messages = await channel.send(f"{r1.mention} {r2.mention} {r3.mention}")
        await messages.delete()
        sql = "INSERT INTO tickets (id, creator) VALUES (%s, %s)"
        self.Cursor.execute(sql, (ticket_id, interaction.user.id))
        self.DB.commit()
        self.Cursor.close()
        self.DB.close()

class TicketSettings(nextcord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @nextcord.ui.button(label="Nutzer Hinzufügen", style=nextcord.ButtonStyle.green, custom_id="TicketSettings:green")
    async def add_user(self, button: nextcord.ui.Button, interaction: Interaction):
        await interaction.response.send_modal(AddUser(interaction.channel))
    
    @nextcord.ui.button(label="Nutzer Entfernen", style=nextcord.ButtonStyle.gray, custom_id="TicketSettings:gray")
    async def remove_user(self, button: nextcord.ui.Button, interaction: Interaction):
        await interaction.response.send_modal(RemoveUser(interaction.channel))
    
    @nextcord.ui.button(label="Ticket Schließen", style=nextcord.ButtonStyle.red, custom_id="TicketSettings:red")
    async def close_ticket(self, button: nextcord.ui.Button, interaction: Interaction):
        self.DB = mysql.connector.connect(
            host="161.97.76.124",
            port=3306,
            user="u138_gx5qKWntiH",
            password="XD13F=Av60OPhh2Y.Fq@5F9k",
            database="s138_dino"
        )
        self.Cursor = self.DB.cursor()
        overwrites = {
            interaction.guild.default_role: nextcord.PermissionOverwrite(read_messages=False),
            interaction.guild.me: nextcord.PermissionOverwrite(read_messages=True, read_message_history=True, send_messages=True, add_reactions=True, manage_messages=True),
            interaction.guild.get_member(interaction.user.id): nextcord.PermissionOverwrite(read_messages=False, read_message_history=False, send_messages=False, add_reactions=False),
            interaction.guild.get_role(1222854878422892634): nextcord.PermissionOverwrite(read_messages=False, read_message_history=False, send_messages=False, add_reactions=False, manage_messages=False),
            interaction.guild.get_role(1222854418710528101): nextcord.PermissionOverwrite(read_messages=False, read_message_history=False, send_messages=False, add_reactions=False, manage_messages=False),
            interaction.guild.get_role(1231237145902059591): nextcord.PermissionOverwrite(read_messages=False, read_message_history=False, send_messages=False, add_reactions=False, manage_messages=False),
            interaction.guild.get_role(1238594607609282652): nextcord.PermissionOverwrite(read_messages=True, read_message_history=True, manage_messages=True),
            interaction.guild.get_role(1238593796489613424): nextcord.PermissionOverwrite(read_messages=True, read_message_history=True, manage_messages=True)
        }
        try:
            channel = interaction.channel.name
            channel_id = channel.split("-")
            new_channel_name = f"Closed-{channel_id[1]}"
            await interaction.channel.edit(name=new_channel_name)
            await interaction.channel.edit(overwrites=overwrites)
            await interaction.response.send_message("Ticket wird geschlossen!", view=ReOpen())
            em = nextcord.Embed(
                title="Erfolgreich",
                description=f"Das Ticket {interaction.channel.name} wurde erfolgreich von {interaction.user.mention} geschlossen!",
                color=nextcord.Color.green()
            )
            sql = "SELECT creator FROM tickets WHERE id = %s"
            self.Cursor.execute(sql, (channel_id[1],)) # Pass the parameter value as a tuple
            user1 = self.Cursor.fetchone()
            if user1 is not None:
                user = interaction.guild.get_member(user1[0])
                if user is not None:
                    await user.send(embed=em)
                else:
                    print(1)
            else:
                print(2)
            sql = "UPDATE tickets SET closed = true, closed_time = CURRENT_TIMESTAMP WHERE id = %s"
            self.Cursor.execute(sql,(channel_id[1],)) # Pass the parameter value as a tuple
            self.DB.commit()
            self.Cursor.close()
            self.DB.close()
        except Exception as e:
            print(f"Error during close ticket process: {e}")
            await interaction.response.send_message("Es gab ein Problem beim Schließen des Tickets. Bitte versuche es erneut.", ephemeral=True)

    @nextcord.ui.button(label="Übernehmen", style=nextcord.ButtonStyle.blurple, custom_id="TicketSettings:blurple")
    async def claim(self, button: nextcord.ui.Button, interaction: Interaction):
        if interaction == None:
            print(10)
        if interaction.channel == None:
            print(20)
        self.DB = mysql.connector.connect(
            host="161.97.76.124",
            port=3306,
            user="u138_gx5qKWntiH",
            password="XD13F=Av60OPhh2Y.Fq@5F9k",
            database="s138_dino"
        )
        self.Cursor = self.DB.cursor()
        roles = [
            1238883285657194578,
            1222854878422892634,
            1222854418710528101,
            1229435879198556192,
            1238593797298851921
        ]
        self.allowed = False
        for role in roles:
            if interaction.user.get_role(role):
                self.allowed = True
            else:
                pass
        if self.allowed == True:
            channel = interaction.channel.name
            channel_id = channel.split("-")
            sql = "UPDATE tickets SET claimed = %s WHERE id = %s"
            self.Cursor.execute(sql, (interaction.user.id, channel_id[1]))
            self.DB.commit()
            sql = "SELECT creator FROM tickets WHERE id = %s"
            self.Cursor.execute(sql, (channel_id[1],)) # Pass the parameter value as a tuple
            user1 = self.Cursor.fetchone()
            em = nextcord.Embed(title="Erfolgreich", description="Dieses ticket wird nun von dir bearbeitet", color=nextcord.Color.green())
            await interaction.response.send_message(embed=em, ephemeral=True)
            button.disabled=True
            em = nextcord.Embed(title="Claim", description=f"Dieses Ticket wird nun von {interaction.user.mention} bearbeitet")
            await interaction.channel.send(f"{user1}", embed=em)
            overwrites = {
                interaction.guild.default_role: nextcord.PermissionOverwrite(read_messages=False),
                interaction.guild.get_member(interaction.user.id): nextcord.PermissionOverwrite(read_messages=True, read_message_history=True, send_messages=True, add_reactions=True, manage_messages=True),
                interaction.guild.get_member(user1): nextcord.PermissionOverwrite(read_messages=True, read_message_history=True, send_messages=True, add_reactions=True),
                interaction.guild.get_role(1238883292372013190): nextcord.PermissionOverwrite(read_messages=True, read_message_history=False, send_messages=False, add_reactions=False, manage_messages=False),
                interaction.guild.get_role(1238883290836897802): nextcord.PermissionOverwrite(read_messages=True, read_message_history=False, send_messages=False, add_reactions=False, manage_messages=False),
                interaction.guild.get_role(1238883285657194578): nextcord.PermissionOverwrite(read_messages=True, read_message_history=False, send_messages=False, add_reactions=False, manage_messages=False),
                interaction.guild.get_role(1231237145902059591): nextcord.PermissionOverwrite(read_messages=True, read_message_history=False, send_messages=False, add_reactions=False, manage_messages=False),
                interaction.guild.get_role(1222854878422892634): nextcord.PermissionOverwrite(read_messages=False, read_message_history=False, send_messages=False, add_reactions=False, manage_messages=False),
                interaction.guild.get_role(1222854418710528101): nextcord.PermissionOverwrite(read_messages=False, read_message_history=False, send_messages=False, add_reactions=False, manage_messages=False),
                interaction.guild.get_role(1229435879198556192): nextcord.PermissionOverwrite(read_messages=False, read_message_history=False, send_messages=False, add_reactions=False, manage_messages=False),
                interaction.guild.get_role(1238593797298851921): nextcord.PermissionOverwrite(read_messages=False, read_message_history=False, send_messages=False, add_reactions=False, manage_messages=False),
                interaction.guild.get_role(1238789598361157683): nextcord.PermissionOverwrite(read_messages=False)
            }
            await interaction.channel.edit(overwrites=overwrites)
            self.Cursor.close()
            self.DB.close()
        else:
            em = nextcord.Embed(title="Fehler", description="Du bist dazu nicht berechtigt", color=nextcord.Color.red())
            await interaction.response.send_message(embed=em)

class ReOpen(nextcord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
    
    @nextcord.ui.button(label="Ticket Wiederöffnen", style=nextcord.ButtonStyle.green, custom_id="ReOpen:green")
    async def re_open(self, button: nextcord.ui.Button, interaction: Interaction):
        self.DB = mysql.connector.connect(
            host="161.97.76.124",
            port=3306,
            user="u138_gx5qKWntiH",
            password="XD13F=Av60OPhh2Y.Fq@5F9k",
            database="s138_dino"
        )
        self.Cursor = self.DB.cursor()
        overwrites = {
            interaction.guild.default_role: nextcord.PermissionOverwrite(read_messages=False),
            interaction.guild.me: nextcord.PermissionOverwrite(read_messages=True, read_message_history=True, send_messages=True, add_reactions=True, manage_messages=True),
            interaction.guild.get_member(interaction.user.id): nextcord.PermissionOverwrite(read_messages=True, read_message_history=True, send_messages=True, add_reactions=True),
            interaction.guild.get_role(1222854878422892634): nextcord.PermissionOverwrite(read_messages=True, read_message_history=True, send_messages=True, add_reactions=True, manage_messages=True),
            interaction.guild.get_role(1222854418710528101): nextcord.PermissionOverwrite(read_messages=True, read_message_history=True, send_messages=True, add_reactions=True, manage_messages=True),
            interaction.guild.get_role(1231237145902059591): nextcord.PermissionOverwrite(read_messages=True, read_message_history=True, send_messages=True, add_reactions=True, manage_messages=True),
            interaction.guild.get_role(1238594607609282652): nextcord.PermissionOverwrite(read_messages=True, read_message_history=True, manage_messages=True),
            interaction.guild.get_role(1238593796489613424): nextcord.PermissionOverwrite(read_messages=True, read_message_history=True, manage_messages=True)
        }
        channel=interaction.channel
        channel_Id = channel.name.split("-")
        sql = "SELCET creator FROM tickets WHERE id = %s"
        self.Cursor.execute(sql, (channel_Id[1]))
        member = self.Cursor.fetchone()
        await interaction.channel.edit(name=f"Ticket-{channel_Id[1]}")
        em = nextcord.Embed(
            title="Wieder Offen",
            description=f"Das Ticket wurde von {interaction.user.mention} wieder geöffnet",
            color=nextcord.Color.green()
        )
        await channel.edit(overwrites=overwrites)
        await interaction.response.send_message(embed=em, view=TicketSettings())
        r1 = interaction.guild.get_role(1222854878422892634)
        r2 = interaction.guild.get_role(1222854418710528101)
        r3 = interaction.guild.get_role(1231237145902059591)
        msg = await channel.send(f"{r1.mention} {r2.mention} {r3.mention} {member.mention}")
        await msg.delete()
        sql = "UPDATE tickets SET closed = false WHERE id = %s"
        self.Cursor.execute(sql, (channel_Id[1]))
        self.DB.commit()
        self.Cursor.close()
        self.DB.close()
    
    @nextcord.ui.button(label="Löschen", style=nextcord.ButtonStyle.red, custom_id="ReOpen:red")
    async def delete(self, button: nextcord.ui.Button, interaction: Interaction):
        self.DB = mysql.connector.connect(
            host="161.97.76.124",
            port=3306,
            user="u138_gx5qKWntiH",
            password="XD13F=Av60OPhh2Y.Fq@5F9k",
            database="s138_dino"
        )
        self.Cursor = self.DB.cursor()
        channel=interaction.channel.name
        channel_id=channel.split("-")
        sql = "UPDATE tickets SET deleted = true, deleted_time = CURRENT_TIMESTAMP WHERE id = %s"
        self.Cursor.execute(sql,(channel_id[1],)) # Pass the parameter value as a tuple
        self.DB.commit()
        self.Cursor.close()
        self.DB.close()
        await interaction.channel.delete()

class SupportCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        self.bot.add_view(CreateTicket())
        self.bot.add_view(TicketSettings())
        self.bot.add_view(ReOpen())
    
    @commands.command()
    async def ticket(self, ctx):
        if ctx.author.get_role(1238117313656651858):
            em = nextcord.Embed(
                title="Unser Support",
                description="Suchst du Hilfe oder willst etwas Reporten?\nDann bist du hier richtig!\nUnsere Teamler sind oftmals 24/7 online, um euch zu helfen.\nDrücke einfach unten auf `Erstelle ein Ticket` und beschreibe dein Problem.\nSpam per erstellen ist verboten.",
                color=0x5865F2
            )
            await ctx.send(embed=em, view=CreateTicket())
    
    @commands.command()
    async def get_user(self, ctx, id):
        try:
            user = ctx.guild.get_member(id)
            await ctx.send(f"{user.mention}", delete_after=30)
        except Exception as e:
            print(e)

def setup(bot):
    bot.add_cog(SupportCog(bot))
