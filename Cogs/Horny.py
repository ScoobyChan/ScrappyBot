
import discord
from discord.ext import commands

def setup(bot):
	settings = bot.get_cog("Settings")
	bot.add_cog(Horny(bot, settings))

class Horny(commands.Cog):
	def __init__(self, bot, settings):
		self.bot = bot
		self.settings = settings

	@commands.command()
	async def horny(self, ctx):
		"""Reminds users what happens when you're horny"""
		await ctx.send('https://tenor.com/view/horny-jail-bonk-dog-hit-head-stop-being-horny-gif-17298755')