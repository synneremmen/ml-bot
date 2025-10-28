# ML Discord Bot

A Discord bot with simple commands to announce coffee or beer breaks in your group chat.

### Installation

Install the Discord library:

```bash
pip install -U discord.py
pip install dotenv
```

### Setup

Create a bot application at https://discord.com/developers/applications and invite it to your server. 
Create an `.env` file in the project directory with 

```
DISCORD_TOKEN=your_bot_token_here
```
To enable logging of your breaks (e.g., lunch and coffee breaks), add the following variables to your `.env` file:

```
LUNSJ_LOG_FILE=lunsj_log.csv
KAFFE_LOG_FILE=kaffe_log.csv
```

These variables specify the file paths where the bot will store the logs for lunch and coffee breaks, respectively.

### Usage

Run the bot:

```bash
python ml-bot.py
```

