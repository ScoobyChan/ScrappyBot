
import asyncio
import os
import json
import urllib.request
import requests
import discord
import random
from discord.ext import commands

async def setup(bot):
	await bot.add_cog(Anime(bot))

class Anime(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		

	@commands.group(pass_context=True)
	async def waifu(self, ctx):
		""" [nsfw/sfw][object]
		Used to send different images of waifu's
		"""
		if ctx.invoked_subcommand is None:
			await ctx.send('Missing  Sub command of sfw or nsfw. eg {0.prefix}waifu sfw '.format(ctx))

	@commands.is_nsfw()
	@waifu.command()
	async def nsfw(self, ctx, _cat=None):
		cat = ['waifu','neko','trap','blowjob']
		response = requests.get("https://waifu.pics/api/{}/{}".format('nsfw', random.choice(cat) if not _cat in cat else _cat))
		if not response: raise Exception(f"Non-success status code: {response.status_code}")
		data = response.json()
		data = data['url']

		if ctx.author.top_role.colour:
			col = ctx.author.top_role.colour
		else:
			col = random.choice(self.bot.color)
		
		embed=discord.Embed(title="Waifu NSFW", color=col)
		embed.set_image(url=data)
		await ctx.send(embed=embed)

	@waifu.command()
	async def sfw(self, ctx, _cat=None):
		cat = ['waifu','neko','shinobu','megumin','bully','cuddle','cry','hug','awoo','kiss','lick','pat','smug','bonk','yeet','blush','smile','wave','smile','wave','highfive','handhold','nom','bite','glomp','kill','slap','happy','wink','poke','dance','cringe','blush']
		response = requests.get("https://waifu.pics/api/{}/{}".format('sfw', random.choice(cat) if not _cat in cat else _cat))
		if not response: raise Exception(f"Non-success status code: {response.status_code}")
		data = response.json()
		data = data['url']

		if ctx.author.top_role.colour:
			col = ctx.author.top_role.colour
		else:
			col = random.choice(self.bot.color)
		
		embed=discord.Embed(title="Waifu SFW", color=col)
		embed.set_image(url=data)
		await ctx.send(embed=embed)