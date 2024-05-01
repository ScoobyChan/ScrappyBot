import json
import urllib.request
import requests
import discord
import random
from discord.ext import commands

async def setup(bot: commands.Bot) -> None:
	settings = bot.get_cog("Settings")
	await bot.add_cog(Animals(bot, settings))

class Animals(commands.Cog):
	def __init__(self, bot, settings):
		self.bot = bot
		self.settings = settings

	@commands.command()
	async def dogapi(self, ctx):
		"""Sends random Dog pics from dog.ceo"""
		with urllib.request.urlopen("https://dog.ceo/api/breeds/image/random") as url:
			data = json.loads(url.read().decode())
			data = data['message']

			if ctx.author.top_role.colour:
				col = ctx.author.top_role.colour
			else:
				col =self.settings.randomColor()
			
			embed=discord.Embed(title="Doggy", color=col)
			embed.set_image(url=data)
			await ctx.send(embed=embed)
			# await ctx.send(data)

	@commands.command()
	async def catstatus(self, ctx):
		"""Sends Random Cats to match the web browser status"""
		status = random.choice(['100','101','102','200','201','202','204','206','207','300','301','302','303','304','305','307','400','401','402','403','404','405','406','408','409','410','411','412','413','414','415','416','417','418','420','421','422','423','424','425','426','429','444','450','451','499','500','501','502','503','504','505','506','507','508','509','510','511','599'])
		# with urllib.request.urlopen("https://http.cat/{}".format(status)) as url:
		# 	data = json.loads(url.read().decode())
			# data = data['embed_url']

		if ctx.author.top_role.colour:
			col = ctx.author.top_role.colour
		else:
			col =self.settings.randomColor()
		
		embed=discord.Embed(title="Cat Status", color=col)
		embed.set_image(url='https://http.cat/{}.jpg'.format(status))
		await ctx.send(embed=embed)

	@commands.group(pass_context=True)
	async def rando(self, ctx):
		"""[Subcommand]
		Please specify what you want ie: dog, cat, floof
		"""
		if ctx.invoked_subcommand is None:
			await ctx.send('Please specify what you want ie: {}rando dog/cat/floof'.format(ctx.prefix))	

	@rando.command(name='cat')
	async def _cat(self, ctx):
		try:
			with urllib.request.urlopen("https://aws.random.cat/meow") as url:
				data = json.loads(url.read().decode())
		except urllib.error.HTTPError as e:
			data = requests.get("https://aws.random.cat/meow")
			data = data.json()

		# print(data['file'])

		if ctx.author.top_role.colour:
			col = ctx.author.top_role.colour
		else:
			col =self.settings.randomColor()
		
		embed=discord.Embed(title="Cat", color=col)
		embed.set_image(url=data['file'])
		await ctx.send(embed=embed)

	@rando.command(name='floof')
	async def _floof(self, ctx):
		try:
			with urllib.request.urlopen("https://randomfox.ca/floof/") as url:
				data = json.loads(url.read().decode())
		except urllib.error.HTTPError as e:
			data = requests.get("https://randomfox.ca/floof/")
			data = data.json()

		# print(data['file'])

		if ctx.author.top_role.colour:
			col = ctx.author.top_role.colour
		else:
			col =self.settings.randomColor()
		
		embed=discord.Embed(title="Floof", color=col)
		embed.set_image(url=data['file'])
		await ctx.send(embed=embed)

	@rando.command(name='dog')
	async def _dog(self, ctx):
		try:
			with urllib.request.urlopen("https://random.dog/woof.json") as url:
				data = json.loads(url.read().decode())
		except urllib.error.HTTPError as e:
			data = requests.get("https://random.dog/woof.json")
			data = data.json()

		# print(data['file'])

		if ctx.author.top_role.colour:
			col = ctx.author.top_role.colour
		else:
			col =self.settings.randomColor()
		
		embed=discord.Embed(title="Doggy", color=col)
		embed.set_image(url=data['file'])
		await ctx.send(embed=embed)

	@commands.group(pass_context=True)
	async def shibe(self, ctx):
		"""[Subcommand]
		Please specify what you want ie: dog, cat, bird
		"""
		if ctx.invoked_subcommand is None:
			await ctx.send('Please specify what you want ie: {}shibe dog/cat/bird'.format(ctx.prefix))	

	@shibe.command(name='cat')
	async def _cat(self, ctx):
		_url = 'http://shibe.online/api/cats?count=1&urls=true&httpsUrls=true'
		data = requests.get(_url)

		if ctx.author.top_role.colour:
			col = ctx.author.top_role.colour
		else:
			col =self.settings.randomColor()
		
		embed=discord.Embed(title="Cat", color=col)
		embed.set_image(url=data.json())
		await ctx.send(embed=embed)

	@shibe.command(name='dog')
	async def _dog(self, ctx):
		_url = 'http://shibe.online/api/shibes?count=1&urls=true&httpsUrls=true'
		data = requests.get(_url)

		if ctx.author.top_role.colour:
			col = ctx.author.top_role.colour
		else:
			col =self.settings.randomColor()
		
		embed=discord.Embed(title="Dogs", color=col)
		embed.set_image(url=data.json())
		await ctx.send(embed=embed)

	@shibe.command(name='bird')
	async def _bird(self, ctx):
		_url = 'http://shibe.online/api/birds?count=1&urls=true&httpsUrls=true'
		data = requests.get(_url)

		if ctx.author.top_role.colour:
			col = ctx.author.top_role.colour
		else:
			col =self.settings.randomColor()
		
		embed=discord.Embed(title="Birds", color=col)
		embed.set_image(url=data.json())
		await ctx.send(embed=embed)