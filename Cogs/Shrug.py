import json
import discord
from discord.ext import commands

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
		self.settings.ServerConfig(ctx.guild.id, 'LastShrug', ctx.author.id)


	# List Permissions For Users
	@commands.command()
	async def lastshrug(self, ctx):
		"""Sends who last shrugged"""
		if self.settings.ServerConfig(ctx.guild.id, 'LastShrug') != 0:
			await ctx.send(f"Last Shrugged: **{self.settings.ServerConfig(ctx.guild.id, 'LastShrug')}**")
		else:
			await ctx.send('No one has Shrugged')
		
def setup(bot):
	settings = bot.get_cog("Settings")
	bot.add_cog(Shrug(bot, settings))