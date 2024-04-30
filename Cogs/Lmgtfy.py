import discord
from discord.ext import commands 
import traceback
import urllib.parse

class Lmgtfy(commands.Cog):
	def __init__(self, bot, settings):
		self.bot = bot
		self.settings = settings

	@commands.command()
	async def lmgt(self, ctx, *, search:str):	
		"""Let me Google that"""
		encoded_query = urllib.parse.quote(search)
		try:
			query_url = f"https://letmegoogleforyou.com/?q={encoded_query}"
			if not ctx.message.author.top_role.colour:
				col = 0xda3c3c
			else:
				col = ctx.message.author.top_role.colour

			embed=discord.Embed(title=query_url, color=col)
			await ctx.send(embed=embed)
		except Exception as e:
			traceback.print_exc()
	
	@commands.command()
	async def lmdt(self, ctx, *, search:str):	
		"""Let me Duckduckgo that"""
		encoded_query = urllib.parse.quote(search)
		try:
			query_url = f"https://lmgtfy2.com/?s=d&q={encoded_query}"
			if not ctx.message.author.top_role.colour:
				col = 0xda3c3c
			else:
				col = ctx.message.author.top_role.colour

			embed=discord.Embed(title=query_url, color=col)
			await ctx.send(embed=embed)
		except Exception as e:
			traceback.print_exc()

async def setup(bot: commands.Bot) -> None:
	settings = bot.get_cog("Settings")
	await bot.add_cog(Lmgtfy(bot, settings))