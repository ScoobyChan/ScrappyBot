import time
import discord
from discord.ext import commands

class Security(commands.Cog):
	# print('Fun Cog Working')
	def __init__(self, bot, settings):
		self.bot = bot
		self.settings = settings

	# Checks:
	# Bot Owners (Makes high up changes)
	# Bot Admins (Lower changes)
	# Claimed (Restrict Usage and commands)
	# Server Owner
	# Server Admins
	# Blacklist Servers (Auto leave if attempted)
	# Permissions Bot has (Admin or General Perms)

async def setup(bot: commands.Bot) -> None:
	settings = bot.get_cog("Settings")
	await bot.add_cog(Security(bot, settings))