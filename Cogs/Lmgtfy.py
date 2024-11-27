import discord
import random
from discord.ext import commands 
import traceback
import urllib

class Lmgtfy(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.URL = "http://tinyurl.com/api-create.php"	

	def shorten(self, url_long):
		try:
			url = self.URL + "?" \
				+ urllib.parse.urlencode({"url": url_long})
			res = requests.get(url)
			return res.text
		except Exception as e:
			raise

	@commands.command()
	async def lmgfy(self, ctx, *, search:str = None):	
		if search:
			try:
				s = self.shorten(f"https://lmgtfy.com/?q={'+'.join(search.split())}")
				if not ctx.message.author.top_role.colour:
					col = random.choice(self.bot.color)
				else:
					col = ctx.message.author.top_role.colour

				embed=discord.Embed(title=s, color=col)
				await ctx.send(embed=embed)
			except Exception as e:
				traceback.print_exc()

def setup(bot):
	bot.add_cog(Lmgtfy(bot))