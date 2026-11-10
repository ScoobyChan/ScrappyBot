import json
import requests
import discord
import aiohttp
import random
from discord.ext import commands

async def setup(bot):
	await bot.add_cog(Personality(bot))

class Personality(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.command()
	async def kanyerest(self, ctx):
		"""
		Gets a Kanye West Quote
		"""
		response = requests.get("https://api.kanye.rest")
		if not response: raise Exception(f"Non-success status code: {response.status_code}")
		data = response.json()

		if ctx.author.top_role.colour:
			col = ctx.author.top_role.colour
		else:
			col = random.choice(self.bot.color)
		
		embed=discord.Embed(title="Kanye West Quotes", description=data['quote'],color=col)
		await ctx.send(embed=embed)
	
	@commands.command()
	async def chucknorris(self, ctx):
		"""
		Gets a Chuck Norris Quote
		"""
		response = requests.get("https://api.chucknorris.io/jokes/random")
		if not response: raise Exception(f"Non-success status code: {response.status_code}")
		data = response.json()

		image = data['icon_url']
		link = data['url']
		description = data['value']
		footer = '[Link]({})'.format(link)

		if ctx.author.top_role.colour:
			col = ctx.author.top_role.colour
		else:
			col = random.choice(self.bot.color)
		
		embed=discord.Embed(title="Chuck Norris", description=description, color=col)
		embed.set_image(url=image)
		await ctx.send(embed=embed)