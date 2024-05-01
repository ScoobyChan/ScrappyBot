import json
import urllib.request
import discord
from discord.ext import commands

async def setup(bot: commands.Bot) -> None:
	settings = bot.get_cog("Settings")
	await bot.add_cog(Personality(bot, settings))

class Personality(commands.Cog):
	def __init__(self, bot, settings):
		self.bot = bot
		self.settings = settings

	@commands.command()
	async def taylorrest(self, ctx):
		"""
		Gets a Taylor Swift Quote
		"""
		with urllib.request.urlopen("https://api.taylor.rest/") as url:
			data = json.loads(url.read().decode())
			data = data['quote']

			if ctx.author.top_role.colour:
				col = ctx.author.top_role.colour
			else:
				col =self.settings.randomColor()
			
			embed=discord.Embed(title="Taylor Swift Quote", description=data['quote'], color=col)
			embed.set_image(url=data)
			await ctx.send(embed=embed)

	@commands.command()
	async def kanyerest(self, ctx):
		"""
		Gets a Kanye West Quote
		"""
		with urllib.request.urlopen("https://api.kanye.rest") as url:
			data = json.loads(url.read().decode())
			if ctx.author.top_role.colour:
				col = ctx.author.top_role.colour
			else:
				col =self.settings.randomColor()
			
			embed=discord.Embed(title="Kanye West Quotes", description=data['quote'],color=col)
			await ctx.send(embed=embed)
		
	@commands.command()
	async def chucknorris(self, ctx):
		"""
		Gets a Chuck Norris Quote
		"""
		with urllib.request.urlopen("https://api.chucknorris.io/jokes/random") as url:
			data = json.loads(url.read().decode())
			image = data['icon_url']
			link = data['url']
			description = data['value']
			footer = '[Link]({})'.format(link)

			desc = description + '\n\n' + footer

			if ctx.author.top_role.colour:
				col = ctx.author.top_role.colour
			else:
				col =self.settings.randomColor()
			
			embed=discord.Embed(title="Chuck Norris", description=description, color=col)
			embed.set_image(url=image)
			await ctx.send(embed=embed)