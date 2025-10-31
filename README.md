# ML Discord Bot

A Discord bot with simple commands to announce coffee or beer breaks in your group chat.

### Installation

Create a virtual environment:

```bash
python -m venv NAME
source NAME/bin/activate
```

Replace NAME with your desired environment name.

To run only the Discord bot, install the core dependencies:

```bash
pip install -U discord.py python-dotenv
```

To enable logging and visualizations, install all dependencies:

```bash
pip install -r requirements.txt
```

### Setup

Create a bot application at https://discord.com/developers/applications and invite it to your server. 
Create an `.env` file in the project directory with 

```
DISCORD_TOKEN=your_bot_token_here
```
To enable logging of your breaks (e.g., lunch and coffee breaks), add the following variables to your `.env` file:

```
LUNSJ_LOG_FILE=logs/lunsj_log.csv
KAFFE_LOG_FILE=logs/kaffe_log.csv
```

These variables specify the file paths where the bot will store the logs for lunch and coffee breaks, respectively.

### Usage

Run the bot:

```bash
python ml-bot.py
```

