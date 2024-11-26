
import asyncio
import os
import json
import urllib.request
import requests
import discord
import aiohttp
import random
from discord.ext import commands

def setup(bot):
	settings = bot.get_cog("Settings")
	bot.add_cog(Coffee(bot, settings))

class Coffee(commands.Cog):
	def __init__(self, bot, settings):
		self.bot = bot
		self.settings = settings

	@commands.command()
	async def coffee(self, ctx):
		"""Coffee API will send coffe pics"""
		with urllib.request.urlopen("https://coffee.alexflipnote.dev/random.json") as url:
			data = json.loads(url.read().decode())
			data = data['file']

			if ctx.author.top_role.colour:
				col = ctx.author.top_role.colour
			else:
				col =self.settings.randomColor()
			
			embed=discord.Embed(title="coffee", color=col)
			embed.set_image(url=data)
			await ctx.send(embed=embed)

