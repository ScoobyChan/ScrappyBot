
import discord
from discord.ext import commands

def setup(bot):
	settings = bot.get_cog("Settings")
	bot.add_cog(Tts(bot, settings))

class Tts(commands.Cog):
	def __init__(self, bot, settings):
		self.bot = bot
		self.settings = settings

	@commands.command()
	async def tts(self, ctx, *, msg):
		"""Lists what I have left to do"""
		await ctx.send(msg, tts=True)