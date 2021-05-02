import random
import urllib.request
import requests
import os
import json
import discord
from discord.ext import commands

imp = 'Json/'
if os.path.exists(imp + 'BotSettings.json'):
	with open(imp + 'BotSettings.json') as t:
		t = json.load(t)
		GIPHY_API = t['GIPHY']

class Giphy(commands.Cog):
	def __init__(self, bot, settings):
		self.bot = bot
		self.settings = settings

	@commands.command()
	async def gif(self, ctx, *, giphy:str=None):
		"""
		[search]
		This searchs for a giph image
		"""
			
		if not giphy:
			with urllib.request.urlopen(f'https://api.giphy.com/v1/gifs/random?api_key={GIPHY_API}&rating=R') as url:
				data = json.loads(url.read().decode())
				data = data['data']
				data = data['embed_url']
		else:
			giphy = giphy.replace(" ", "+")
			with urllib.request.urlopen(f"http://api.giphy.com/v1/gifs/search?q={giphy}&api_key={GIPHY_API}&limit=1&rating=R") as url:
				data = json.loads(url.read().decode())
				data = random.choice(data['data'])
				data = data['embed_url']

		if ctx.author.top_role.colour:
			col = ctx.author.top_role.colour
		else:
			col =self.settings.randomColor()

		embed=discord.Embed(title=f"Gif", color=col)
		embed.set_image(url=data)
		await ctx.send(embed=embed)
		# await ctx.send(data)

def setup(bot):
	settings = bot.get_cog("Settings")
	bot.add_cog(Giphy(bot, settings))