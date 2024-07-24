import nextcord
from nextcord import Interaction
from nextcord.ext import commands
import datetime

class BanCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(name="ban", description="Bant eine person", default_member_permissions=nextcord.Permissions(ban_members=True))
    async def ban(self, interaction: Interaction, user: nextcord.Member, nachrichten_löschen: int = 0, grund: str = "Kein Grund"):
        if user == interaction.user:
            await interaction.response.send_message("Du kannst dich nicht bannen!", ephemeral=True)
        elif user.bot:
            await interaction.response.send_message("Ich werde keine Bots Bannen versuche /kick", ephemeral=True)
        elif user.get_role(1238117313656651858):
            if interaction.user.get_role(1238593796489613424):
                await interaction.response.send_message(f"{user.mention} wurde gebannt!", ephemeral=True)
                return await user.ban(delete_message_days=nachrichten_löschen, reason=reason)
            else:
                return await interaction.response.send_message("Du kannst keine Team Mitglieder Bannen", ephemeral=True)
        else:
            await user.ban(delete_message_days=nachrichten_löschen, reason=reason)
            await interaction.response.send_message(f"{user.mention} wurde gebannt!", ephemeral=True)

    #@nextcord.slash_command(name="unban", description="Unbant eine person", default_member_permissions=nextcord.Permissions(ban_members=True), guild_ids=[1180167998342975578, 1217146612472610928])
    #async def unban(self, interaction: Interaction, user_id: str, reason: str = "Kein Grund"):
    #    for ban in interaction.guild.bans():
    #        if user_id == ban.user.id:
    #            if user_id == interaction.user.id:
    #                await interaction.response.send_message("Du kannst dich nicht entbannen!", ephemeral=True)
    #            else:
    #                user = interaction.client.get_user(user_id)
    #                await interaction.guild.unban(user, reason)
    #                await interaction.response.send_message(f"{user.name} wurde entbannt!", ephemeral=True)
    #        else:
    #            await interaction.response.send_message("Dieser Nutzer ist nicht gebannt", ephemeral=True)
    
    @nextcord.slash_command(name="kick", description="kickt eine person", default_member_permissions=nextcord.Permissions(kick_members=True))
    async def kick(self, interaction: Interaction, user: nextcord.Member, reason: str = "Kein Grund"):
        if user == interaction.user:
            return await interaction.response.send_message("Du kannst dich nicht kicken!", ephemeral=True)
        elif user.get_role(1238117313656651858):
            if interaction.user.get_role(1238593796489613424):
                await user.kick(reason=reason)
                await interaction.response.send_message(f"{user.name} wurde gekickt", ephemeral=True)
            else:
                return await interaction.response.send_message("Du kannst keine Team Mitglieder Kicken!", ephemeral=True)
        else:
            await user.kick(reason=reason)
            await interaction.response.send_message(f"{user.name} wurde gekickt", ephemeral=True)

    @nextcord.slash_command(name="timeout", description="Timeoutet eine person", default_member_permissions=nextcord.Permissions(mute_members=True))
    async def timeout(self, interaction: Interaction, user: nextcord.Member, duration: int, reason: str = "Kein Grund"):
        if user == interaction.user:
            return await interaction.response.send_message("Du kannst dich nicht timeouten!", ephemeral=True)
        elif user.bot:
            return await interaction.response.send_message("Du kannst keine Bost timeouten!", ephemeral=True)
        elif user.get_role(1238117313656651858):
            if interaction.user.get_role(1238593796489613424):
                await interaction.response.send_message(f"Nutzer {user.mention} wurde für {duration} minuten gemutet", ephemeral=True)
                return await user.timeout(timeout=nextcord.utils.utcnow() + datetime.timedelta(minutes=duration), reason=reason)
            else:
                return await interaction.response.send_message("Du kannst keine Team Mitglieder Timeouten", ephemeral=True)
        else:
            await user.timeout(timeout=nextcord.utils.utcnow() + datetime.timedelta(minutes=duration), reason=reason)
            await interaction.response.send_message(f"Nutzer {user.mention} wurde für {duration} minuten gemutet", ephemeral=True)

def setup(bot):
    bot.add_cog(BanCog(bot))