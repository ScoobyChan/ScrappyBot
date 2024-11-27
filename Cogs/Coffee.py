import json
import requests
import discord
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
		response = requests.get("https://coffee.alexflipnote.dev/random.json")
		if not response: raise Exception(f"Non-success status code: {response.status_code}")
		data = response.json()
		data = data['file']

		if ctx.author.top_role.colour:
			col = ctx.author.top_role.colour
		else:
			col =  random.choice(self.bot.color)
		
		embed=discord.Embed(title="coffee", color=col)
		embed.set_image(url=data)
		await ctx.send(embed=embed)
