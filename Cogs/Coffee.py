
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
	bot.add_cog(Coffee(bot))

class Coffee(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.command()
	async def coffee(self, ctx):
		"""Coffee API will send coffe pics"""
		with urllib.request.urlopen("https://coffee.alexflipnote.dev/random.json") as url:
			data = json.loads(url.read().decode())
			data = data['file']

			if ctx.author.top_role.colour:
				col = ctx.author.top_role.colour
			else:
				col =  random.choice(self.bot.color)
			
			embed=discord.Embed(title="coffee", color=col)
			embed.set_image(url=data)
			await ctx.send(embed=embed)

