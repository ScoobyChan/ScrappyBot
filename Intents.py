import discord

# intents = discord.Intents.all()
# intents = discord.Intents.default()
# intents = discord.Intents.none()

# Extra intents for specific settings
intents = discord.Intents.none()
intents.bans = True
intents.dm_messages = True
intents.dm_reactions = True
intents.dm_typing = True
intents.emojis = True
intents.guild_messages = True
intents.guild_reactions = True
intents.guild_typing = True
intents.guilds = True
intents.integrations = True
intents.invites = True
intents.members = True
intents.messages = True
intents.presences = True
intents.reactions = True
intents.typing = True
intents.voice_states = True
intents.webhooks = True