import random
import discord
import requests
import urllib.request
import bs4

# https://stackoverflow.com/questions/276052/how-to-get-current-cpu-and-ram-usage-in-python

from discord.ext import commands


class ImgurSearch(commands.Cog):
	def __init__(self, bot, settings):
		self.settings = settings
		self.bot = bot

	async def imgurSearch(self, ctx, query):
		query = "+".join(query.split(' '))
		try:
			url = f'http://imgur.com/search?q={query}'
			while not url.endswith('#'):
				req = urllib.request.Request(url)
				page = urllib.request.urlopen(req)
				bs = bs4.BeautifulSoup(page,"html.parser")
				print(page.read().decode())
				# for images in bs.find_all('img'):
				# 	print(images.get('src'))
				await ctx.send("http:"+str(random.choice(bs.find_all('img')).get('src')))
				break

		except urllib.error.HTTPError as err:
			# print("Error Status:", err)
			await ctx.send(err)

	@commands.command()
	async def imgur(self, ctx, *, query=None):
		"""
		[image]
		searches imgur for images
		"""			
		if not query: return await ctx.send('No search given')
		await self.imgurSearch(ctx, query)
		

def setup(bot):
	settings = bot.get_cog("Settings")
	bot.add_cog(ImgurSearch(bot, settings))