import json
import urllib.request
import requests
import discord
import random
from discord.ext import commands
from imgurpython import ImgurClient
		
class Api(commands.Cog):
	def __init__(self, bot, settings):
		self.bot = bot
		self.settings = settings

	@commands.command()
	async def kitty(self, ctx):
		"""Kitty"""

		with urllib.request.urlopen('http://aws.random.cat//meow') as url:
			data = json.loads(url.read().decode())
			# print(data['file'])
			if ctx.author.top_role.colour:
				col = ctx.author.top_role.colour
			else:
				col =self.settings.randomColor()

			embed=discord.Embed(title="Kitty Cats :cat:", color=col)
			embed.set_image(url=data['file'])
			await ctx.send(embed=embed)

	@commands.command()
	async def doggo(self, ctx):
		"""**Doggies**"""
		with urllib.request.urlopen('https://random.dog/woof.json') as url:
			data = json.loads(url.read().decode())
			# print(data['url'])
			if ctx.author.top_role.colour:
				col = ctx.author.top_role.colour
			else:
				col =self.settings.randomColor()

			embed=discord.Embed(title="Dogs :dog:", color=col)
			embed.set_image(url=data['url']);
			await ctx.send(embed=embed)

	@commands.command()
	async def moredogs(self, ctx):
		"""More Dogs"""

		with urllib.request.urlopen("https://dog.ceo/api/breeds/image/random") as url:
			data = json.loads(url.read().decode())
			# print(data['message'])
			if ctx.author.top_role.colour:
				col = ctx.author.top_role.colour
			else:
				col =self.settings.randomColor()

			embed=discord.Embed(title="More Dogs :dog2:", color=col)
			embed.set_image(url=data['message']);
			await ctx.send(embed=embed)

	@commands.command()
	async def boobs(self, ctx):
		"""Boob Pics"""
		await ctx.message.delete()

		with urllib.request.urlopen("http://api.oboobs.ru/boobs") as url:
			data = json.loads(url.read().decode())

			if ctx.author.top_role.colour:
				col = ctx.author.top_role.colour
			else:
				col =self.settings.randomColor()

			t = True
			while t:
				rdm = random.randint(0, data[0]['id'])
				boob = "http://media.oboobs.ru/boobs_preview/{}.jpg".format(rdm)
				r = requests.get(boob)
				if r.status_code == 400:
					pass
				elif r.status_code == 404:
					pass
				else:
					break

			embed=discord.Embed(title="Boobs", color=col)
			embed.set_image(url=boob);
			await ctx.send(embed=embed)

	@commands.command()
	async def butts(self, ctx):
		"""Butt Pics"""
		await ctx.message.delete()

		with urllib.request.urlopen("http://api.obutts.ru/butts") as url:
			data = json.loads(url.read().decode())

			if ctx.author.top_role.colour:
				col = ctx.author.top_role.colour
			else:
				col =self.settings.randomColor()

			t = True
			while t:
				rdm = random.randint(0, data[0]['id'])
				butt = "http://media.obutts.ru/butts_preview/0{}.jpg".format(rdm)
				r = requests.get(butt)
				if r.status_code == 400:
					pass
				elif r.status_code == 404:
					pass
				else:
					break
					
			embed=discord.Embed(title="Butts", color=col)
			embed.set_image(url=butt);
			await ctx.send(embed=embed)

	@commands.command()
	async def dankmeme(self, ctx):
		"""Sends dank memes"""

		with urllib.request.urlopen(f"http://api.giphy.com/v1/gifs/search?q=dankmeme&api_key={self.bot.GIPHY_API}&limit=1&rating=R") as url:
			data = json.loads(url.read().decode())
			data = random.choice(data['data'])
			data = data['embed_url']

		if ctx.author.top_role.colour:
			col = ctx.author.top_role.colour
		else:
			col =self.settings.randomColor()
		
		embed=discord.Embed(title=f"Dank Meme", color=col)
		embed.set_image(url=data)
		# await ctx.send(embed=embed)
		await ctx.send(data)

	@commands.command()
	async def classicCars(self, ctx):
		"""Sends classic Cars"""

		with urllib.request.urlopen(f"http://api.giphy.com/v1/gifs/search?q=classiccars&api_key={self.bot.GIPHY_API}&limit=1&rating=R") as url:
			data = json.loads(url.read().decode())
			data = random.choice(data['data'])
			data = data['embed_url']

		if ctx.author.top_role.colour:
			col = ctx.author.top_role.colour
		else:
			col =self.settings.randomColor()
		
		embed=discord.Embed(title=f"Classic Cars", color=col)
		embed.set_image(url=data)
		# await ctx.send(embed=embed)
		await ctx.send(data)

	@commands.command()
	async def classictrucks(self, ctx):
		"""Sends classic trucks"""

		with urllib.request.urlopen(f"http://api.giphy.com/v1/gifs/search?q=classictrucks&api_key={self.bot.GIPHY_API}&limit=1&rating=R") as url:
			data = json.loads(url.read().decode())
			data = random.choice(data['data'])
			data = data['embed_url']

		if ctx.author.top_role.colour:
			col = ctx.author.top_role.colour
		else:
			col =self.settings.randomColor()
		
		embed=discord.Embed(title=f"Classic Trucks", color=col)
		embed.set_image(url=data)
		# await ctx.send(embed=embed)
		await ctx.send(data)

	@commands.command()
	async def meme(self, ctx):
		"""Sends memes I hope"""

		with urllib.request.urlopen(f"http://api.giphy.com/v1/gifs/search?q=meme&api_key={self.bot.GIPHY_API}&limit=1&rating=R") as url:
			data = json.loads(url.read().decode())
			data = random.choice(data['data'])
			data = data['embed_url']

		if ctx.author.top_role.colour:
			col = ctx.author.top_role.colour
		else:
			col =self.settings.randomColor()

		embed=discord.Embed(title=f"Meme", color=col)
		embed.set_image(url=data)
		# await ctx.send(embed=embed)
		await ctx.send(data)

	@commands.command()
	async def goose(self, ctx):
		"""Goose"""

		with urllib.request.urlopen(f"http://api.giphy.com/v1/gifs/search?q=goose&api_key={self.bot.GIPHY_API}&limit=1&rating=R") as url:
			data = json.loads(url.read().decode())
			data = random.choice(data['data'])
			data = data['embed_url']

		if ctx.author.top_role.colour:
			col = ctx.author.top_role.colour
		else:
			col =self.settings.randomColor()

		embed=discord.Embed(title=f"Goose", color=col)
		embed.set_image(url=data)
		# await ctx.send(embed=embed)
		await ctx.send(data)

	@commands.command()
	async def kea(self, ctx):
		"""Kea"""

		with urllib.request.urlopen(f"http://api.giphy.com/v1/gifs/search?q=kea&api_key={self.bot.GIPHY_API}&limit=1&rating=R") as url:
			data = json.loads(url.read().decode())
			data = random.choice(data['data'])
			data = data['embed_url']

		if ctx.author.top_role.colour:
			col = ctx.author.top_role.colour
		else:
			col =self.settings.randomColor()

		embed=discord.Embed(title=f"Kea", color=col)
		embed.set_image(url=data)
		# await ctx.send(embed=embed)
		await ctx.send(data)

	@commands.command()
	async def sheep(self, ctx):
		"""Sheep"""
			
		with urllib.request.urlopen(f"http://api.giphy.com/v1/gifs/search?q=sheep&api_key={self.bot.GIPHY_API}&limit=1&rating=R") as url:
			data = json.loads(url.read().decode())
			data = random.choice(data['data'])
			data = data['embed_url']
			data = json.loads(url.read().decode())

		if ctx.author.top_role.colour:
			col = ctx.author.top_role.colour
		else:
			col =self.settings.randomColor()

		embed=discord.Embed(title=f"Sheep", color=col)
		embed.set_image(url=data)
		# await ctx.send(embed=embed)
		await ctx.send(data)		

async def setup(bot: commands.Bot) -> None:
	settings = bot.get_cog("Settings")
	await bot.add_cog(Api(bot, settings))