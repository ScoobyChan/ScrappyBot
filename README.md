# ScrappyBot
# Generative AI was used for some files
# Minimum requirement
Python 3.10 or newer is required for the Bot to operate
Lavalink is required to be setup too for Music to be operational

# Installation
Install requirements with: 

```bash
python -m venv .venv
```

Activate the environment:

```powershell
.\.venv\Scripts\Activate.ps1
```

On macOS/Linux, use `source .venv/bin/activate`.

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

Create a `.env` file in the same folder as `Scrappy.py`:

```
PREFIX=""
TOKEN=""
MARIADB_HOST="127.0.0.1"
MARIADB_PORT="3306"
MARIADB_USER="scrappybot"
MARIADB_PASSWORD=""
MARIADB_DATABASE="scrappybot"
```

Without PREFIX, default will be set to $, Without TOKEN, the bot will not be able to integrate to discord

For PostgreSQL, configure these variables instead:

```
POSTGRES_HOST="127.0.0.1"
POSTGRES_PORT="5432"
POSTGRES_USER="scrappybot"
POSTGRES_PASSWORD=""
POSTGRES_DATABASE="scrappybot"
```

## Ollama

The Ollama cog uses a local Ollama server for chat. Set these optional
environment variables to choose the server and model; web search additionally
requires an Ollama API key from https://ollama.com/settings/keys:

```
OLLAMA_HOST="http://localhost:11434"
OLLAMA_MODEL="qwen3.5:4b"
OLLAMA_API_KEY=""
```

Pull the configured model in Ollama before using chat. The `chat` (alias:
`ollama`) command keeps a short conversation per user and channel; use
`chat clear` to reset it. `websearch <query>` returns Ollama web-search results.
`messagesearch <query>` (alias: `msgsearch`) searches up to the latest 500
messages in the current channel and returns up to five matches. The bot needs
permission to read message history in that channel.

The MariaDB and PostgreSQL cogs are optional and load only when their respective
host variable is configured. Each creates a `bot_settings` table in its
configured database and provides asynchronous `get_value`, `set_value`, and
`delete_value` methods. They do not migrate or replace the existing JSON/YAML
settings. Create the database and user beforehand; the configured user needs
permission to create the table and select, insert, update, and delete rows.
