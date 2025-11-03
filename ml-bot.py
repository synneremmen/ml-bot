import datetime
import os
import time
import discord
from discord.ext import commands
from dotenv import load_dotenv
load_dotenv()
from utils import initialize_log_file, log_event

LUNSJ_LOG_FILE = None
KAFFE_LOG_FILE = None
BORDTENNIS_LOG_FILE = None
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

should_log_lunsj = os.getenv("LUNSJ_LOG_FILE") is not None
should_log_kaffe = os.getenv("KAFFE_LOG_FILE") is not None
should_log_bordtennis = os.getenv("BORDTENNIS_LOG_FILE") is not None

if should_log_lunsj:
    lunsj_start_time = None
    LUNSJ_LOG_FILE = os.getenv("LUNSJ_LOG_FILE")
    initialize_log_file(LUNSJ_LOG_FILE)
if should_log_kaffe:
    kaffe_start_time = None
    KAFFE_LOG_FILE = os.getenv("KAFFE_LOG_FILE")
    initialize_log_file(KAFFE_LOG_FILE)
if should_log_bordtennis:
    bordtennis_start_time = None
    BORDTENNIS_LOG_FILE = os.getenv("BORDTENNIS_LOG_FILE")
    initialize_log_file(BORDTENNIS_LOG_FILE)

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
            "`$kaffe` - Start en kaffepause for alle!\n"
            "`$kaffestopp` - Avslutt kaffepausen og få alle tilbake til arbeidet!\n"
            "`$lunsj` - Start en lunsjpause for alle!\n"
            "`$lunsjstopp` - Avslutt lunsjpausen og få alle tilbake til arbeidet!\n"
            "`$bordtennis` - Kall alle inn til bordtennis!\n"
            "`$bordtennisstopp` - Avslutt bordtennis!\n"
            "`$øl` - Kall alle inn til en øl!\n"
        )

    if "$kaffestopp" in message.content.lower():
        kaffe_end_time = time.time()
        # ensure coffee duration is reasonable and existing
        if kaffe_start_time and kaffe_start_time < kaffe_end_time and (kaffe_end_time - kaffe_start_time) < 2 * 60 * 60:  # less than 2 hours
            minutes = log_event(kaffe_start_time, kaffe_end_time, KAFFE_LOG_FILE)
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
            minutes = log_event(lunsj_start_time, lunsj_end_time, LUNSJ_LOG_FILE)
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
            minutes = log_event(bordtennis_start_time, bordtennis_end_time, BORDTENNIS_LOG_FILE)
            await message.channel.send(f"Bordtennispausen er over, tilbake til arbeidet! Bordtennispausen varte i {minutes} minutter.")
        else:
            await message.channel.send(f"Bordtennispausen er over, tilbake til arbeidet!")

    elif "$bordtennis" in message.content.lower():
        if should_log_bordtennis:
            bordtennis_start_time = time.time()
        await message.channel.send(f"Game on! {message.author.mention} er klar for bordtennis! @everyone 🏓")


    if "$øl" in message.content.lower():
        await message.channel.send(f"{message.author.mention} trenger en øl, så nå må @everyone stille opp 🍺")

    await bot.process_commands(message)


if __name__ == "__main__":
    if not DISCORD_TOKEN:
        print("Error: set DISCORD_TOKEN environment variable with your bot token.")
    else:
        bot.run(DISCORD_TOKEN)