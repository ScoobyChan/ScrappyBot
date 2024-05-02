import discord
from discord.ext import commands
import urllib.parse


class Steam(commands.Cog):
	def __init__(self, bot, settings):
		self.bot = bot
		self.settings = settings

	def clean(self, s):
		s = s.replace(' ', '+')
		s = s.replace('\\', '\\\\')
		s = s.replace('http://', 'www.')
		s = s.replace('https://', 'www.')

		return s

	@commands.command()
	async def SteamGames(self, ctx, *, search:str):
		"""
		[Game to search]
		Searchs for steam games
		"""
		encoded_query = urllib.parse.quote(search)
		steam_search = f'https://store.steampowered.com/search/?term={encoded_query}'
		await ctx.send(steam_search)
		

	@commands.command()
	async def SteamMarket(self, ctx, *, search:str=None):
		"""
		[Market Item to search]
		Search for market item
		"""
		encoded_query = urllib.parse.quote(search)
		steam_search = f'https://steamcommunity.com/market/search?q={encoded_query}'
		await ctx.send(steam_search)
		

async def setup(bot: commands.Bot) -> None:
	settings = bot.get_cog("Settings")
	await bot.add_cog(Steam(bot, settings))