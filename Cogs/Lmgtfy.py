import discord
from discord.ext import commands 
from Utils import TinyURL
import traceback

class Lmgtfy(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.command()
	async def lmgfy(self, ctx, *, search:str = None):	
		if search:
			try:
				obj = TinyURL.Tinyurl()
				s = obj.shorten(f"https://lmgtfy.com/?q={'+'.join(search.split())}")
				if not ctx.message.author.top_role.colour:
					col = 0xda3c3c
				else:
					col = ctx.message.author.top_role.colour

				embed=discord.Embed(title=s, color=col)
				await ctx.send(embed=embed)
			except Exception as e:
				traceback.print_exc()

def setup(bot):
	bot.add_cog(Lmgtfy(bot))