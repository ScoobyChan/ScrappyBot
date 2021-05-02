import discord
from discord.ext import commands

from Scripts import Utils

class Steam(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.UT = Utils.Utils()

	def clean(self, s):
		s = s.replace(' ', '+')
		s = s.replace('\\', '\\\\')
		s = s.replace('http://', 'www.')
		s = s.replace('https://', 'www.')

		return s

	@commands.command()
	async def SteamGames(self, ctx, *, s:str=None):
		"""
		[Game to search]
		Searchs for steam games
		"""
		if not s:
			return await ctx.send('No search has been made')

		s = self.clean(s)
		bing = f'https://store.steampowered.com/search/?term={s}'
		await ctx.send(self.UT.shorten(bing))
		

	@commands.command()
	async def SteamMarket(self, ctx, *, s:str=None):
		"""
		[Market Item to search]
		Search for market item
		"""
		if not s:
			return await ctx.send('No search has been made')

		s = self.clean(s)
		bing = f'https://steamcommunity.com/market/search?q={s}'
		await ctx.send(self.UT.shorten(bing))
		

def setup(bot):
	bot.add_cog(Steam(bot))