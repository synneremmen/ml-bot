import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="$", intents=intents, help_command=None)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (id: {bot.user.id})")


@bot.event
async def on_message(message: discord.Message):
    if message.author.bot:
        return

    if "$help" in message.content.lower():
        await message.channel.send(
            "Hei! Jeg er en enkel bot som hjelper med kaffepauser og ølpauser.\n"
            "Bruk følgende kommandoer:\n"
            "`$help` - Vis denne hjelpen.\n"
            "`$kaffe` - Start en kaffepause for alle!\n"
            "`$kaffestopp` - Avslutt kaffepausen og få alle tilbake til arbeidet!\n"
            "`$øl` - Start en ølpause for alle!\n"
        )

    if "$kaffestopp" in message.content.lower():
        await message.channel.send(f"Kaffepausen er ferdig, @everyone tilbake til arbeidet!")
    
    elif "$kaffe" in message.content.lower():
        await message.channel.send(f"Nå har {message.author.mention} lyst på kaffe, så nå må @everyone ta en kaffepause! ☕")
    
    if "$øl" in message.content.lower():
        await message.channel.send(f"{message.author.mention} trenger en øl, så nå må @everyone stille opp 🍺")

    await bot.process_commands(message)


if __name__ == "__main__":
    if not DISCORD_TOKEN:
        print("Error: set DISCORD_TOKEN environment variable with your bot token.")
    else:
        bot.run(DISCORD_TOKEN)