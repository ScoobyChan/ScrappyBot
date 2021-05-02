import traceback
import discord
from discord.ext import commands 
from Scripts import Utils

class TinyURL(commands.Cog):
	def __init__(self, bot, settings):
		self.bot = bot
		self.Utils = Utils.Utils()
		self.settings = settings

	@commands.command()
	async def tinyurl(self, ctx, *, search:str = None):
		"""
		[url]
		Produces a tiny url or an url
		"""

		if search:
			if search[:5] == 'https' or search[:4] ==  'http' or search[:3] ==  'www':
				try:
					s = self.Utils.shorten(search)

					if ctx.author.top_role.colour:
						col = ctx.author.top_role.colour
					else:
						col =self.settings.randomColor()
						
					embed=discord.Embed(title=s, color=col)
					await ctx.send(embed=embed)
				except Exception as e:
					traceback.print_exc()
					
def setup(bot):
	settings = bot.get_cog("Settings")
	bot.add_cog(TinyURL(bot, settings))