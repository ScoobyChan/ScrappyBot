import random
import discord
from discord.ext import commands

from Utils import Utils

def setup(bot):
	settings = bot.get_cog("Settings")
	bot.add_cog(Color(bot, settings))

class Color(commands.Cog):
	def __init__(self, bot, settings):
		self.bot = bot
		self.settings = settings
		self.Utils = Utils.Utils()

	@commands.command()
	async def color(self, ctx, col):
		"""[color]
		Provides an Embed of the color specified which could be a hex or discord colors
		"""
		try:
			if col.startswith('#'):
				col = col.replace('#', '0x')
			val = int(col, 16)
			color=discord.Color(val)
			print(val)
			print(color)
		except ValueError:
			Fuzz = self.bot.get_cog('FuzzySearch')
			if not Fuzz:	
				if not col in self.bot.color:
					return await ctx.send('Cannot find the color {} in my list. heres the list: {}'.format(col, color))
			else:
				col = Fuzz.fuzSearch(col, self.bot.color)
				
			color = self.bot.color[col]


		embed = discord.Embed(
			description = ('Color: **%s**' % col),
			colour = color
		)
		await ctx.send(embed=embed)

	@commands.command()
	async def liststrcolor(self, ctx):
		"""[]
		Lists the different colors using embeds
		"""
		for col in self.bot.color:
			embed = discord.Embed(
				description = ('Color: \n %s' % col),
				colour = col
			)
			await ctx.send(embed=embed)