import json
import discord
from discord.ext import commands
from datetime import datetime
import pytz

class Shrug(commands.Cog):
	def __init__(self, bot, settings):
		self.bot = bot
		self.settings = settings

	# List Permissions For Bot/Users
	@commands.command()
	async def shrug(self, ctx):
		"""Shrugs Emoji"""

		await ctx.message.delete()
		await ctx.send('¯\\_(ツ)_/¯')
		
		utc_now = datetime.fromisoformat(datetime.now()).strftime('%Y-%m-%d %H:%M:%S %Z')
		self.settings.database(ctx, 'Update_Item', 'Guilds', item_id=ctx.guild.id, value_id='shrug', content=[ctx.author.id, str(utc_now)])

	# List Permissions For Users
	@commands.command()
	async def lastshrug(self, ctx):
		"""Sends who last shrugged"""
		shrug = self.settings.database(ctx, 'Get_Item', 'Guilds', item_id=ctx.guild.id, value_id='shrug')
		if shrug:
			for u, d in shrug: 
				await ctx.send(f"{u} Last Shrugged on {d}") # Convert Time to TZ, convert User ID to Username/Nick
		else:
			await ctx.send('No one has Shrugged')
		
async def setup(bot: commands.Bot) -> None:
	settings = bot.get_cog("Settings")
	await bot.add_cog(Shrug(bot, settings))