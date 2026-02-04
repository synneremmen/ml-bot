import datetime
import os
import re
import time
import discord
from discord.ext import commands
from dotenv import load_dotenv
load_dotenv()
from utils import get_tournament_mentions, initialize_log_file, log_event
import csv
import editdistance

def get_log_file(name, titles=["timestamp", "duration"]):
    should_log = True if os.getenv(f"{name}_LOG_FILE") is not None else False
    if should_log:
        LOG_FILE = os.getenv(f"{name}_LOG_FILE")
        initialize_log_file(LOG_FILE, titles)
        start_time = None
        return LOG_FILE, should_log, start_time
    return None, False

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
KAFFE_LOG_FILE, should_log_kaffe, kaffe_start_time = get_log_file("KAFFE")
LUNSJ_LOG_FILE, should_log_lunsj, lunsj_start_time = get_log_file("LUNSJ")
BORDTENNIS_LOG_FILE, should_log_bordtennis, bordtennis_start_time = get_log_file("BORDTENNIS")
KONGE_LOG_FILE, _, _ = get_log_file("KONGE", titles=["timestamp", "konge"])
MONARK_LOG_FILE, _, _ = get_log_file("MONARK", titles=["timestamp", "monark"])
WORDLE_LOG_FILE, _, _ = get_log_file("WORDLE", titles=["timestamp", "stats"])
ALLOWED_BOT_IDS = [int(bot_id) for bot_id in os.getenv("ALLOWED_BOT_IDS").split(",")]
MAX_TOURNAMENT_PARTICIPANTS = 5
tournament_list = []

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="$", intents=intents, help_command=None)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (id: {bot.user.id})")

@bot.event
async def on_message(message: discord.Message):
    global kaffe_start_time, lunsj_start_time, bordtennis_start_time
    global tournament_list

    command = re.search(r'\$([A-Za-z]+)\b', message.content).group(1) if re.search(r'\$([A-Za-z]+)\b', message.content) else ""

    if message.author.bot and message.author.id not in ALLOWED_BOT_IDS:
        return
    
    if message.author.id in ALLOWED_BOT_IDS and "yesterday's results" in message.content.lower(): # look for worlde bot and results
        result = message.content.splitlines()
        for line in result[1:]: # first line is an unrelevant message
            match = re.match(r'^\s*(?:👑\s*)?(\d+)/6:\s*(.+)', line)
            if match:
                score = match.group(1)
                users = match.group(2).split(' ')
                for user in users:
                    user = user.strip()
                    if user:
                        log_event(f"{user} - {score}/6", WORDLE_LOG_FILE, is_time=False)


    if editdistance.eval(command, "help") <= 2:
        await message.channel.send(
            "Hei! Jeg er en enkel bot som hjelper med kaffepauser og ølpauser.\n"
            "Bruk følgende kommandoer:\n"
            "`$help` - Vis denne hjelpen.\n"
            "`$øl` - Kall alle inn til en øl!\n"
            "`$kalender` - Kall alle inn til å åpne julekalenderen!\n"
            "`$monark` - Nåværende monark av uno\n"
            "`$nymonark @bruker` - Sett en ny monark av uno\n"
            "`$kaffe` - Start en kaffepause for alle!\n"
            "`$kaffestopp` - Avslutt kaffepausen og få alle tilbake til arbeidet!\n"
            "`$lunsj` - Start en lunsjpause for alle!\n"
            "`$lunsjstopp` - Avslutt lunsjpausen og få alle tilbake til arbeidet!\n"
            "`$konge` - Nåværende konge av bordtennis\n"
            "`$nykonge @bruker` - Sett en ny konge av bordtennis\n"
            "`$deltaker` - Legg deg selv til som deltaker i bordtennisturneringen!\n"
            "`$bordtennis` - Kall alle inn til bordtennis! Hvis flere enn maks deltakere, blir det delt inn i grupper. Husk å avslutte runden/spillet med $bordtennisstopp!\n"
            "`$bordtennisstopp` - Hvis en turnering pågår, henter dette en ny gruppe. Ellers, avslutt bordtennis!\n"
        )

    if editdistance.eval(command, "kaffestopp") <= 2:
        kaffe_end_time = time.time()
        # ensure coffee duration is reasonable and existing
        if kaffe_start_time and kaffe_start_time < kaffe_end_time and (kaffe_end_time - kaffe_start_time) < 2 * 60 * 60:  # less than 2 hours
            duration = int(kaffe_end_time - kaffe_start_time)
            minutes = log_event(duration, KAFFE_LOG_FILE)
            await message.channel.send(f"Kaffepausen er ferdig, tilbake til arbeidet! Kaffepausen varte i {minutes} minutter.")
        else:
            await message.channel.send(f"Kaffepausen er ferdig, tilbake til arbeidet!")
    
    elif editdistance.eval(command, "kaffe") <= 2:
        if should_log_kaffe:
            kaffe_start_time = time.time()
        await message.channel.send(f"Nå har {message.author.mention} lyst på kaffe, så nå må @everyone ta en kaffepause! ☕")

    if editdistance.eval(command, "lunsjstopp") <= 2:
        lunsj_end_time = time.time()
        # ensure lunch duration is reasonable and existing
        if lunsj_start_time and lunsj_start_time < lunsj_end_time and (lunsj_end_time - lunsj_start_time) < 1.5 * 60 * 60:  # less than 1.5 hours
            duration = int(lunsj_end_time - lunsj_start_time)
            minutes = log_event(duration, LUNSJ_LOG_FILE)
            await message.channel.send(f"Lunsjpausen er over, tilbake til arbeidet! Lunsjpausen varte i {minutes} minutter.")
        else:
            await message.channel.send(f"Lunsjpausen er over, tilbake til arbeidet!")

    elif editdistance.eval(command, "lunsj") <= 2:
        if should_log_lunsj:
            lunsj_start_time = time.time()
        await message.channel.send(f"Ding ding ding! {message.author.mention} er sulten, så la oss ta en lunsjpause! @everyone 🍽️")

    if editdistance.eval(command, "bordtennisstopp") <= 2:
        if tournament_list:
            mentions, tournament_list = get_tournament_mentions(tournament_list, MAX_TOURNAMENT_PARTICIPANTS)
            await message.channel.send(f"På tide med en ny gruppe! {mentions} - Gjør dere klare for bordtennis! 🏓")

        else: # if no tournament ongoing, log duration: ensure bordtennis duration is reasonable and existing
            bordtennis_end_time = time.time()
            if bordtennis_start_time and bordtennis_start_time < bordtennis_end_time and (bordtennis_end_time - bordtennis_start_time) < 1.5 * 60 * 60:  # less than 1.5 hours
                duration = int(bordtennis_end_time - bordtennis_start_time)
                minutes = log_event(duration, BORDTENNIS_LOG_FILE)
                await message.channel.send(f"Bordtennispausen er over, tilbake til arbeidet! Bordtennispausen varte i {minutes} minutter.")
            else:
                await message.channel.send(f"Bordtennispausen er over, tilbake til arbeidet!")

    elif editdistance.eval(command, "bordtennis") <= 2:
        if should_log_bordtennis:
            bordtennis_start_time = time.time()

        if tournament_list:
            mentions, tournament_list = get_tournament_mentions(tournament_list, MAX_TOURNAMENT_PARTICIPANTS)
            await message.channel.send(f"{mentions} - Gjør dere klare for bordtennis! 🏓")
        else:
            await message.channel.send(f"Game on! {message.author.mention} er klar for bordtennis! @everyone 🏓")

    if editdistance.eval(command, "deltaker") <= 2:
        participant = message.author        
        if participant not in tournament_list:    
            tournament_list.append(participant)
            await message.channel.send(f"{participant.mention} er lagt til som deltaker i turneringen!")
        else:
            await message.channel.send(f"{participant.mention}, du er allerede registrert som deltaker i turneringen!")

    if editdistance.eval(command, "kalender") <= 2:
        await message.channel.send(f"God {datetime.datetime.now().day}. desember @everyone! Alle store og små troll må bevege seg til Mimmi, for nå skal vi åpne julekalenderen! 🎄")


    if "$øl" in message.content.lower():
        await message.channel.send(f"{message.author.mention} trenger en øl, så nå må @everyone stille opp 🍺")


    if editdistance.eval(command, "konge") <= 1:
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

    if editdistance.eval(command, "nykonge") <= 1:
        split = message.content.split()
        if len(split) >= 2:
            new_king = log_event(split[1], KONGE_LOG_FILE, is_time=False)
            await message.channel.send(f"{new_king} er nå den nye kongen av bordtennis! 👑")
        else:
            await message.channel.send("Vennligst spesifiser en bruker for å sette som ny konge, f.eks. `$nykonge @bruker`.")

    if editdistance.eval(command, "monark") <= 1:
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
        
    if editdistance.eval(command, "nymonark") <= 1:
        split = message.content.split()
        if len(split) >= 2:
            new_monarch = log_event(split[1], MONARK_LOG_FILE, is_time=False)
            await message.channel.send(f"{new_monarch} er nå den nye monarken av uno! 👑")
        else:
            await message.channel.send("Vennligst spesifiser en bruker for å sette som ny monark, f.eks. `$nymonark @bruker`.")


if __name__ == "__main__":
    if not DISCORD_TOKEN:
        print("Error: set DISCORD_TOKEN environment variable with your bot token.")
    else:
        bot.run(DISCORD_TOKEN)