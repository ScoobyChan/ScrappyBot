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

	# @commands.command()
	# async def foaas(self, ctx, to_member: discord.Member = None, from_member: discord.Member = None):
	# 	"""
	# 	Tells people to F*** off basically
	# 	"""
	# 	if not from_member:	from_member = "Everyone"
	# 	if not to_member:	to_member = ctx.author

	# 	if to_member.top_role.colour:
	# 		col = to_member.top_role.colour
	# 	else:
	# 		col =self.settings.randomColor()
		
	# 	to_member = to_member.nick if to_member.nick else to_member.name

	# 	desc = fuck.off(name=to_member, from_=from_member).text

	# 	embed=discord.Embed(description=desc, color=col)
	# 	await ctx.send(embed=embed)

	# @commands.command()
	# async def foaasr(self, ctx, to_member: discord.Member = None, from_member: discord.Member = None):
	# 	"""
	# 	"""
	# 	if not from_member:	from_member = "Everyone"
	# 	if not to_member:	to_member = ctx.author

	# 	if to_member.top_role.colour:
	# 		col = to_member.top_role.colour
	# 	else:
	# 		col =self.settings.randomColor()
		
	# 	to_member = to_member.nick if to_member.nick else to_member.name

	# 	desc = fuck.random(name=to_member, from_=from_member).text

	# 	embed=discord.Embed(description=desc, color=col)
	# 	await ctx.send(embed=embed)

	@commands.command()
	async def dicksize(self, ctx, member: discord.Member = None):
		if not member:
			member = ctx.author

		size = len(member.nick) if member.nick else len(member.name)
		await ctx.send(f'{member.nick if member.nick else member.name}\'s dick size is {size}\" \n8{"="*size}D')

