from datetime import datetime
import os
import signal
import time
import colorama
import subprocess
import nextcord
from nextcord.ext import commands
import mysql.connector
import readchar
from assets.config import F, S, environ, logo

def get_time():
    now = datetime.now()
    dt_string = now.strftime("%Y-%m-%d %H:%M:%S")
    return dt_string

os.system("clear")
print("--------------------------------------------------------------------------------------------------------------")
print(F.b + S.D + logo.logo + F.R_ALL)
print("--------------------------------------------------------------------------------------------------------------")
print(" ")
print(F.y + S.D + "[" + get_time() + "] " + S.N + "[INFO]" + F.R + " Nextcord verison:")
print(F.y + S.D + "[" + get_time() + "] " + F.R_ALL + "       " + nextcord.__version__)
print(" ")
print(F.y + S.D + "[" + get_time() + "] " + S.N + "[INFO]" + F.R + " Colorama version:")
print(F.y + S.D + "[" + get_time() + "] " + F.R_ALL + "       " + colorama.__version__)
print(" ")
print("--------------------------------------------------------------------------------------------------------------")

intents = nextcord.Intents.all()
bot = commands.AutoShardedBot(command_prefix=commands.when_mentioned_or("!"), intents=intents)
bot.remove_command("help")

cogs_c = "cogs.commands"
cogs_e = "cogs.events"
cogs_t = "cogs.tasks"
cogs_o = "cogs.other"

cogs = [
    f"{cogs_c}.ban",
    f"{cogs_c}.embed",
    f"{cogs_c}.ping",
    #f"{cogs_o}.voice",
    f"{cogs_o}.bewerben",
    f"{cogs_o}.tickets",
    #f"{cogs_e}.mao",
    f"{cogs_e}.on_message",
    #f"{cogs_e}.on_error",
    f"{cogs_e}.welcome"
]

print(" ")
print(F.y + S.D + "[" + get_time() + "] " + S.N + "[INFO]" + F.R + " Laden von Cogs . . .")
for cog in cogs:
    if cog.startswith("cogs.commands.embeds"):
        try:
            bot.load_extension(cog)
        except Exception as e:
            cog=cog.split(".")
            print(F.y + S.D + "[" + get_time() + "] " + S.N + F.r + "       [ERROR]" + F.R + " Konnte den Cog " + cog[3] + " nicht laden: " + str(e) + "!")
        else:
            cog = cog.split(".")
            print(F.y + S.D + "[" + get_time() + "] " + S.B + F.g + "       [SUCCESSFULY]" + F.R_ALL + " Embed " + cog[3] + " wurde geladen.")

    elif any(cog.startswith(i) for i in [cogs_c, cogs_e, cogs_c, cogs_o]):
        try:
            bot.load_extension(cog)
        except Exception as e:
            cog=cog.split(".")
            print(F.y + S.D + "[" + get_time() + "] " + S.N + F.r + "       [ERROR]" + F.R + " Konnte den Cog " + cog[2] + " nicht laden: " + str(e) + "!")
        else:
            cog = cog.split(".")
            print(F.y + S.D + "[" + get_time() + "] " + F.g + S.B + "       [SUCCESSFULY]" + F.R_ALL + " Cog " + cog[2] + " wurde geladen.")
    else:
        print(F.y + S.D + "[" + get_time() + "] " + S.N + F.r + "       [ERROR]" + F.R + cog + " ist eine unbekannte Datei")

print(" ")
print("--------------------------------------------------------------------------------------------------------------")

def handler(signum, frame):
    msg = "\nCtrl-c was pressed. Do you really want to exit? y/n "
    print(msg, end="", flush=True)
    res = readchar.readchar()
    if res == 'y':
        print("", end="\r", flush=True)
        print(" " * len(msg), end="", flush=True) # clear the printed line
        print("    ", end="\r", flush=True)
        print("--------------------------------------------------------------------------------------------------------------")
        print(" ")
        print(" ")
        print(F.y + S.D + "[" + get_time() + "] " + F.g + S.B + "[SUCCESSFULY]" + F.R_ALL + " Bot wurde gestopt.")
        print(" ")
        print(" ")
        print("--------------------------------------------------------------------------------------------------------------")
        exit()
    else:
        print("", end="\r", flush=True)
        print(" " * len(msg), end="", flush=True) # clear the printed line
        print("    ", end="\r", flush=True)

signal.signal(signal.SIGINT, handler)

@bot.event
async def on_ready():
    print(" ")
    print(F.y + S.D + "[" + get_time() + "] " + F.g + S.B + "[SUCCESSFULY]" + F.R_ALL + " Discord Bot wurde gestartet.")
    print(" ")
    try:
        mysql.connector.connect(
        	host="161.97.76.124",
            port=3306,
            user="u138_gx5qKWntiH",
            password="XD13F=Av60OPhh2Y.Fq@5F9k",
            database="s138_dino"
        )
        print(F.y + S.D + "[" + get_time() + "] " + F.g + S.B + "[SUCCESSFULY]" + F.R_ALL + " MySQL wurde Verbunden.")
    except Exception as e:
        print(e)
        exit()
    print(" ")
    print(F.y + S.D + "[" + get_time() + "] " + S.N + "[INFO]" + F.R + " Eingelogt als:")
    print(F.y + S.D + "[" + get_time() + "] " + F.R_ALL + "       " + bot.user.name)
    print(" ")
    print(F.y + S.D + "[" + get_time() + "] " + S.N + F.y + "[INFO]" + F.R + " Bot ID:")
    print(F.y + S.D + "[" + get_time() + "] " + F.R_ALL + "       " + str(bot.user.id))
    print(" ")
    print("--------------------------------------------------------------------------------------------------------------")
    print(" ")
    #await bot.sync_application_commands(guild_id=1180167998342975578)

environ()

bot.run(os.environ["TOKEN"])