import datetime
import os
import time
import discord
from discord.ext import commands
from dotenv import load_dotenv
load_dotenv()
from utils import initialize_log_file, log_event
import csv

def init_log_file(name, titles=["timestamp", "duration_seconds"]):
    should_log = True if os.getenv(f"{name}_LOG_FILE") is not None else False
    if should_log:
        LOG_FILE = os.getenv(f"{name}_LOG_FILE")
        initialize_log_file(LOG_FILE, titles)
        start_time = None
        return LOG_FILE, should_log, start_time
    return None, False

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
KAFFE_LOG_FILE, should_log_kaffe, kaffe_start_time = init_log_file("KAFFE")
LUNSJ_LOG_FILE, should_log_lunsj, lunsj_start_time = init_log_file("LUNSJ")
BORDTENNIS_LOG_FILE, should_log_bordtennis, bordtennis_start_time = init_log_file("BORDTENNIS")
KONGE_LOG_FILE, _, _ = init_log_file("KONGE", titles=["timestamp", "konge"])
MONARK_LOG_FILE, _, _ = init_log_file("MONARK", titles=["timestamp", "monark"])


intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="$", intents=intents, help_command=None)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (id: {bot.user.id})")


@bot.event
async def on_message(message: discord.Message):
    global kaffe_start_time, lunsj_start_time, bordtennis_start_time

    if message.author.bot:
        return

    if "$help" in message.content.lower():
        await message.channel.send(
            "Hei! Jeg er en enkel bot som hjelper med kaffepauser og ølpauser.\n"
            "Bruk følgende kommandoer:\n"
            "`$help` - Vis denne hjelpen.\n"
            "`$øl` - Kall alle inn til en øl!\n"
            "`$konge` - Nåværende konge av bordtennis\n"
            "`$nykonge @bruker` - Sett en ny konge av bordtennis\n"
            "`$monark` - Nåværende monark av uno\n"
            "`$nymonark @bruker` - Sett en ny monark av uno\n"
            ""
            "   Logging kommandoer (hvis aktivert):\n"
            "`$kaffe` - Start en kaffepause for alle!\n"
            "`$kaffestopp` - Avslutt kaffepausen og få alle tilbake til arbeidet!\n"
            "`$lunsj` - Start en lunsjpause for alle!\n"
            "`$lunsjstopp` - Avslutt lunsjpausen og få alle tilbake til arbeidet!\n"
            "`$bordtennis` - Kall alle inn til bordtennis!\n"
            "`$bordtennisstopp` - Avslutt bordtennis!\n"
        )

    if "$kaffestopp" in message.content.lower():
        kaffe_end_time = time.time()
        # ensure coffee duration is reasonable and existing
        if kaffe_start_time and kaffe_start_time < kaffe_end_time and (kaffe_end_time - kaffe_start_time) < 2 * 60 * 60:  # less than 2 hours
            duration = int(kaffe_end_time - kaffe_start_time)
            minutes = log_event(duration, KAFFE_LOG_FILE)
            await message.channel.send(f"Kaffepausen er ferdig, tilbake til arbeidet! Kaffepausen varte i {minutes} minutter.")
        else:
            await message.channel.send(f"Kaffepausen er ferdig, tilbake til arbeidet!")
    
    elif "$kaffe" in message.content.lower():
        if should_log_kaffe:
            kaffe_start_time = time.time()
        await message.channel.send(f"Nå har {message.author.mention} lyst på kaffe, så nå må @everyone ta en kaffepause! ☕")

    if "$lunsjstopp" in message.content.lower():
        lunsj_end_time = time.time()
        # ensure lunch duration is reasonable and existing
        if lunsj_start_time and lunsj_start_time < lunsj_end_time and (lunsj_end_time - lunsj_start_time) < 1.5 * 60 * 60:  # less than 1.5 hours
            duration = int(lunsj_end_time - lunsj_start_time)
            minutes = log_event(duration, LUNSJ_LOG_FILE)
            await message.channel.send(f"Lunsjpausen er over, tilbake til arbeidet! Lunsjpausen varte i {minutes} minutter.")
        else:
            await message.channel.send(f"Lunsjpausen er over, tilbake til arbeidet!")

    elif "$lunsj" in message.content.lower():
        if should_log_lunsj:
            lunsj_start_time = time.time()
        await message.channel.send(f"Ding ding ding! {message.author.mention} er sulten, så la oss ta en lunsjpause! @everyone 🍽️")

    if "$bordtennisstopp" in message.content.lower():
        bordtennis_end_time = time.time()
        # ensure bordtennis duration is reasonable and existing
        if bordtennis_start_time and bordtennis_start_time < bordtennis_end_time and (bordtennis_end_time - bordtennis_start_time) < 1.5 * 60 * 60:  # less than 1.5 hours
            duration = int(bordtennis_end_time - bordtennis_start_time)
            minutes = log_event(duration, BORDTENNIS_LOG_FILE)
            await message.channel.send(f"Bordtennispausen er over, tilbake til arbeidet! Bordtennispausen varte i {minutes} minutter.")
        else:
            await message.channel.send(f"Bordtennispausen er over, tilbake til arbeidet!")

    elif "$bordtennis" in message.content.lower():
        if should_log_bordtennis:
            bordtennis_start_time = time.time()
        await message.channel.send(f"Game on! {message.author.mention} er klar for bordtennis! @everyone 🏓")


    if "$øl" in message.content.lower():
        await message.channel.send(f"{message.author.mention} trenger en øl, så nå må @everyone stille opp 🍺")


    if "$konge" in message.content.lower():
        if KONGE_LOG_FILE and os.path.exists(KONGE_LOG_FILE):
            with open(KONGE_LOG_FILE, newline='') as f:
                reader = csv.reader(f)
                rows = [row for row in reader if any(cell.strip() for cell in row)]
            if rows and len(rows) > 1:
                konge = rows[-1][-1].strip()
                await message.channel.send(f"Nåværende konge av bordtennis er {konge} 👑")
            else:
                await message.channel.send("Det er ingen konge av bordtennis ennå. Sett en med `$nykonge @bruker`.")
        else:
            await message.channel.send("Det er ingen konge av bordtennis ennå. Sett en med `$nykonge @bruker`.")

    if "$nykonge" in message.content.lower():
        split = message.content.split()
        if len(split) >= 2:
            new_king = log_event(split[1], KONGE_LOG_FILE, is_time=False)
            await message.channel.send(f"{new_king} er nå den nye kongen av bordtennis! 👑")
        else:
            await message.channel.send("Vennligst spesifiser en bruker for å sette som ny konge, f.eks. `$nykonge @bruker`.")

    if "$monark" in message.content.lower():
        if MONARK_LOG_FILE and os.path.exists(MONARK_LOG_FILE):
            with open(MONARK_LOG_FILE, newline='') as f:
                reader = csv.reader(f)
                rows = [row for row in reader if any(cell.strip() for cell in row)]
            if rows and len(rows) > 1:
                monark = rows[-1][-1].strip()
                await message.channel.send(f"Nåværende monark av uno er {monark} 👑")
            else:
                await message.channel.send("Det er ingen monark av uno ennå. Sett en med `$nymonark @bruker`.")
        else:
            await message.channel.send("Det er ingen monark av uno ennå. Sett en med `$nymonark @bruker`.")
        
    if "$nymonark" in message.content.lower():
        split = message.content.split()
        if len(split) >= 2:
            new_monarch = log_event(split[1], MONARK_LOG_FILE, is_time=False)
            await message.channel.send(f"{new_monarch} er nå den nye monarken av uno! 👑")
        else:
            await message.channel.send("Vennligst spesifiser en bruker for å sette som ny monark, f.eks. `$nymonark @bruker`.")

    await bot.process_commands(message)


if __name__ == "__main__":
    if not DISCORD_TOKEN:
        print("Error: set DISCORD_TOKEN environment variable with your bot token.")
    else:
        bot.run(DISCORD_TOKEN)