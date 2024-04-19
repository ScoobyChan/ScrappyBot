from foaas import fuck 
import asyncio
import os
import json
import urllib.request
import requests
import discord
import aiohttp
import random
from discord.ext import commands

async def setup(bot: commands.Bot) -> None:
	settings = bot.get_cog("Settings")
	await bot.add_cog(Social(bot, settings))

class Social(commands.Cog):
	def __init__(self, bot, settings):
		self.bot = bot
		self.settings = settings
		if self.bot.get_cog('Perms'):
			self.bot.nsfw.append('Social')
		

	@commands.command()
	async def foaas(self, ctx, _to, _from='Everyone'):
		"""[to object] [from object]
		Tells people to F*** off basically
		"""
		if ctx.author.top_role.colour:
			col = ctx.author.top_role.colour
		else:
			col =self.settings.randomColor()
		
		desc = fuck.off(name=_to, from_=_from).text

		embed=discord.Embed(description=desc, color=col)
		await ctx.send(embed=embed)

	@commands.command()
	async def dicksize(self, ctx, member: discord.Member = None):
		if not member:
			member = ctx.author

		size = len(member.nick) if member.nick else len(member.name)
		await ctx.send(f'{member.nick if member.nick else member.name}\'s dick size is {size}\" \n8{"="*size}D')

