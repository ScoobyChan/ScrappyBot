
import asyncio
import json
import urllib.request
import requests
import discord
import aiohttp
import random
from discord.ext import commands

async def setup(bot):
	await bot.add_cog(Animals(bot))

class Animals(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.command()
	async def dogapi(self, ctx):
		"""Sends random Dog pics from dog.ceo"""
		with urllib.request.urlopen("https://dog.ceo/api/breeds/image/random") as url:
			data = json.loads(url.read().decode())
			data = data['message']

			if ctx.author.top_role.colour:
				col = ctx.author.top_role.colour
			else:
				col = random.choice(self.bot.color)
			
			embed=discord.Embed(title="Doggy", color=col)
			embed.set_image(url=data)
			await ctx.send(embed=embed)
			# await ctx.send(data)

	@commands.command()
	async def catstatus(self, ctx):
		"""Sends Random Cats to match the web browser status"""
		status = random.choice(['100','101','102','200','201','202','204','206','207','300','301','302','303','304','305','307','400','401','402','403','404','405','406','408','409','410','411','412','413','414','415','416','417','418','420','421','422','423','424','425','426','429','444','450','451','499','500','501','502','503','504','505','506','507','508','509','510','511','599'])
		
		if ctx.author.top_role.colour:
			col = ctx.author.top_role.colour
		else:
			col = random.choice(self.bot.color)
		
		embed=discord.Embed(title="Cat Status", color=col)
		embed.set_image(url='https://http.cat/{}.jpg'.format(status))
		await ctx.send(embed=embed)