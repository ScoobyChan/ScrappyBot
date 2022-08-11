import json
import urllib
import requests
import discord
from discord.ext import commands

class Search(commands.Cog):
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

	def clean(self, s):
		s = s.replace(' ', '+')
		s = s.replace('\\', '\\\\')
		s = s.replace('http://', 'www.')
		s = s.replace('https://', 'www.')

		return s

	@commands.command()
	async def bing(self, ctx, *, s:str=None):
		"""
		[search]
		searches bing
		"""
		if not s:
			return await ctx.send('No search has been made')

		s = self.clean(s)
		bing = f"https://www.bing.com/search?q={s}&qs=n&form=QBRE&sp=-1&pq=test+hello&sc=6-10&sk=&cvid=B8D48DAD49B54CD59C1852CAB85ED9AB"
		await ctx.send(self.shorten(bing))

	@commands.command()
	async def wiki(self, ctx, *, s:str=None):
		"""
		[search]
		searches wikipedia
		"""
		if not s:
			return await ctx.send('No search has been made')

		s = self.clean(s)
		s = s.replace('+', '_')
		bing = f"https://en.wikipedia.org/wiki/{s}"
		await ctx.send(self.shorten(bing))

	@commands.command()
	async def pbtech(self, ctx, *, s:str=None):
		"""
		[search]
		searches PB Technology
		"""
		if not s:
			return await ctx.send('No search has been made')

		s = self.clean(s)
		bing = f"https://www.pbtech.co.nz/search?sf={s}&search_type="
		await ctx.send(self.shorten(bing))

	@commands.command()
	async def duckduckgo(self, ctx, *, s:str=None):
		"""
		[search]
		searches duck duck go
		"""
		if not s:
			return await ctx.send('No search has been made')

		s = self.clean(s)
		bing = f"https://duckduckgo.com/?q={s}&t=h_&ia=about"
		await ctx.send(self.shorten(bing))

	@commands.command()
	async def github(self, ctx, *, s:str=None):
		"""
		[search]
		searches github
		"""
		if not s:
			return await ctx.send('No search has been made')

		s = self.clean(s)
		bing = f"https://github.com/search?q={s}"
		await ctx.send(self.shorten(bing))

	@commands.command()
	async def youtube(self, ctx, *, s:str=None):
		"""
		[search]
		searches youtube
		"""
		if not s:
			return await ctx.send('No search has been made')

		s = self.clean(s)
		bing = f"https://www.youtube.com/results?search_query={s}"
		await ctx.send(self.shorten(bing))

	@commands.command()
	async def yahoo(self, ctx, *, s:str=None):
		"""
		[search]
		searches yahoo
		"""
		if not s:
			return await ctx.send('No search has been made')

		s = self.clean(s)
		bing = f"https://nz.search.yahoo.com/search?p={s}&fr=yfp-t&fp=1&toggle=1&cop=mss&ei=UTF-8"
		await ctx.send(self.shorten(bing))
		
	@commands.command()
	async def stackoverflow(self, ctx, *, s:str=None):
		"""
		[search]
		searches stackoverflow
		"""
		if not s:
			return await ctx.send('No search has been made')

		s = self.clean(s)
		bing = f"https://stackoverflow.com/search?q={s}"
		await ctx.send(self.shorten(bing))

	@commands.command()
	async def reddit(self, ctx, *, s:str=None):
		"""
		[search]
		searches reddit
		"""
		if not s:
			return await ctx.send('No search has been made')

		s = self.clean(s)
		bing = f"https://www.reddit.com/search/?q={s}"
		await ctx.send(self.shorten(bing))

	@commands.command()
	async def amazon(self, ctx, *, s:str=None):
		"""
		[search]
		searches amazon
		"""
		if not s:
			return await ctx.send('No search has been made')

		s = self.clean(s)
		bing = f"https://www.amazon.com/s?k={s}&ref=nb_sb_noss_1"
		await ctx.send(self.shorten(bing))

def setup(bot):
	bot.add_cog(Search(bot))