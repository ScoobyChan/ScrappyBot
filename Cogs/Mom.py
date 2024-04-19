
import discord
from discord.ext import commands

async def setup(bot: commands.Bot) -> None:
	settings = bot.get_cog("Settings")
	await bot.add_cog(Mom(bot, settings))

class Mom(commands.Cog):
	def __init__(self, bot, settings):
		self.bot = bot
		self.settings = settings

	@commands.command(aliases=['mom', 'mum'])
	async def urmom(self, ctx):
		"""Sends out ur mom"""
		await ctx.send('**Ur mom**')

	@commands.command()
	async def urmama(self, ctx):
		"""Your mama jokes"""
		with urllib.request.urlopen("https://www.yomama-jokes.com/api/v1/jokes/random/") as url:
			data = json.loads(url.read().decode())
			_data = data['joke']

			await ctx.send(_data)