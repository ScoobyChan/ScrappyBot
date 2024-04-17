
import discord
from discord.ext import commands

async def setup(bot: commands.Bot) -> None:
	settings = bot.get_cog("Settings")
	await bot.add_cog(Mom(bot, settings))

class Mom(commands.Cog):
	def __init__(self, bot, settings):
		self.bot = bot
		self.settings = settings

	# Add Message Checker like No u and honk

	@commands.command(aliases=['mom', 'mum'])
	async def urmom(self, ctx):
		"""Sends out ur mom"""
		await ctx.send('**Ur mom**')