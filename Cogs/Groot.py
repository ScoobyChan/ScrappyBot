# Credits CorpNewt for 
# https://github.com/corpnewt/CorpBot.py/blob/rewrite/Cogs/Groot.py

import random
import discord
from discord.ext import commands

class Groot(commands.Cog):
	# print('Fun Cog Working')
	def __init__(self, bot, settings):
		self.bot = bot
		self.settings = settings

	@commands.command()
	async def groot(self, ctx):
		"""
		I am Groot?
		"""
		groot = ['Groot','*Groot*','**Groot**','***Groot***','Groot...']
		i = ['i','*i*','**i**','i...','*i...*','**i...**']
		am = ['am','*am*','**am**','am...','*am...*','**am...**']
		c = random.choice(i) +' '+ random.choice(am) +' '+ random.choice(groot)
		await ctx.send(c)

def setup(bot):
	settings = bot.get_cog("Settings")
	bot.add_cog(Groot(bot, settings))