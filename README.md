# ScrappyBot
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

The MariaDB cog is optional. When configured, it creates a `bot_settings` table
and provides asynchronous `get_value`, `set_value`, and `delete_value` methods.
It does not migrate or replace the existing JSON/YAML settings. Create the
database and user beforehand; the configured user needs permission to create
the table and select, insert, update, and delete rows.
