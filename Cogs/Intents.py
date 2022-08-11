import discord
from discord.ext import commands

def setup(bot):
	settings = bot.get_cog("Settings")
	bot.add_cog(Intents(bot, settings))

class Intents(commands.Cog):
	def __init__(self, bot, settings):
		self.bot = bot
		self.settings = settings

	@commands.command()
	async def intents(self, ctx):
		"""Lists Intents of Bot"""
		intents = discord.Intents.all()
		intent = '\n'.join(['{}: {}'.format(x, y) for x, y in intents])
		embed=discord.Embed(title="Bot Intents", description=intent, color=self.settings.randomColor())		
		await ctx.send(embed=embed)