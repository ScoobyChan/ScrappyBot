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
		
		current_datetime = datetime.now()
		formatted_date = current_datetime.strftime('%d-m-%Y %H:%M:%S')
		self.settings.database(ctx, 'Update_Item', 'Guilds', item_id=ctx.guild.id, value_id='shrug', content=[ctx.author.id, str(formatted_date)])

	# List Permissions For Users
	@commands.command()
	async def lastshrug(self, ctx):
		"""Sends who last shrugged"""
		last_shrugged = self.settings.database(ctx, 'Get_Item', 'Guilds', item_id=ctx.guild.id, value_id='shrug')
		last_shrugged_user = await self.settings.get_username_by_id(ctx, last_shrugged[0])
		# last_shrugged_time = self.settings.convert_time(last_shrugged[1], 'Pacific/Auckland')
		last_shrugged_time = last_shrugged[1]
		# print(last_shrugged)
		if last_shrugged:
			await ctx.send(f"**{last_shrugged_user}** Last Shrugged on **{last_shrugged_time}**") # Convert Time to TZ, convert User ID to Username/Nick
		else:
			await ctx.send('No one has Shrugged')
		
async def setup(bot: commands.Bot) -> None:
	settings = bot.get_cog("Settings")
	await bot.add_cog(Shrug(bot, settings))