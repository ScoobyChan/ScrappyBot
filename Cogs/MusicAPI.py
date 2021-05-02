
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
	settings = bot.get_cog("Settings")
	bot.add_cog(MusicAPI(bot, settings))

class MusicAPI(commands.Cog):
	def __init__(self, bot, settings):
		self.bot = bot
		self.settings = settings

	@commands.group(pass_context=True)
	async def itunes(self, ctx):
		"""[Subcommand][to search]
		In reality this just checks if a subcommand is being invoked.
		Usage: $itunes id/name 'id'/'name'
		Subcomands include:
		id [id]
		name [name]
		"""
			
		if ctx.invoked_subcommand is None:
			await ctx.send('No, {0.subcommand_passed} is not cool'.format(ctx))

	@itunes.command(name='id')
	async def _ID(self, ctx, _id):

		# To work on
		url = "https://itunes.apple.com/term?id={}&limit=1".format(_id)
		try:
			with urllib.request.urlopen(url) as url:
				data = json.loads(url.read().decode())
		except urllib.error.HTTPError as e:
			requests.get(url)
			data = data.json()

		data = data['results'][0]

		if ctx.author.top_role.colour:
			col = ctx.author.top_role.colour
		else:
			col =self.settings.randomColor()
		
		CollectionName = data['collectionName']
		ArtistName = data['artistName']
		ArtistID = data['artistId']
		Type = data['kind']
		Genre = data['primaryGenreName']
		TrackNumber = data['trackNumber']
		TrackPrice = data['trackPrice']
		Explicitness = data['trackExplicitness']
		ReleaseDate = data['releaseDate']
		artworkUrl100 = data['artworkUrl100']
		TrackURL = data['trackViewUrl']

		embed=discord.Embed(title="{}({})".format(ArtistName, ArtistID), color=col)
		embed.set_image(url=artworkUrl100)
		embed.add_field(name="CollectionName", value=CollectionName, inline=True)
		embed.add_field(name="Type", value=Type, inline=True)
		embed.add_field(name="Genre", value=Genre, inline=True)
		embed.add_field(name="TrackNumber", value=TrackNumber, inline=True)
		embed.add_field(name="TrackPrice", value=TrackPrice, inline=True)
		embed.add_field(name="Explicitness", value=Explicitness, inline=True)
		embed.add_field(name="artworkUrl100", value=artworkUrl100, inline=True)
		embed.set_footer(text=ReleaseDate)
		await ctx.send(embed=embed)

	@itunes.command(name='name')
	async def _NAME(self, ctx, *, _id):
		# To work on
		_id = '+'.join(_id.split(' '))
		url = "https://itunes.apple.com/search?term={}&limit=1".format(_id)
		try:
			with urllib.request.urlopen(url) as url:
				data = json.loads(url.read().decode())
		except urllib.error.HTTPError as e:
			requests.get(url)
			data = data.json()

		data = data['results'][0]

		if ctx.author.top_role.colour:
			col = ctx.author.top_role.colour
		else:
			col =self.settings.randomColor()
		
		CollectionName = data['collectionName']
		ArtistName = data['artistName']
		ArtistID = data['artistId']
		Type = data['kind']
		Genre = data['primaryGenreName']
		TrackNumber = data['trackNumber']
		TrackPrice = data['trackPrice']
		Explicitness = data['trackExplicitness']
		ReleaseDate = data['releaseDate']
		artworkUrl100 = data['artworkUrl100']
		TrackURL = data['trackViewUrl']

		embed=discord.Embed(title="{}({})".format(ArtistName, ArtistID), color=col)
		embed.set_image(url=artworkUrl100)
		embed.add_field(name="CollectionName", value=CollectionName, inline=True)
		embed.add_field(name="Type", value=Type, inline=True)
		embed.add_field(name="Genre", value=Genre, inline=True)
		embed.add_field(name="TrackNumber", value=TrackNumber, inline=True)
		embed.add_field(name="TrackPrice", value=TrackPrice, inline=True)
		embed.add_field(name="Explicitness", value=Explicitness, inline=True)
		embed.add_field(name="artworkUrl100", value=artworkUrl100, inline=True)
		embed.set_footer(text=ReleaseDate)
		await ctx.send(embed=embed)

	# @commands.command()
	# async def spotify(self, ctx, url):
	# 	with urllib.request.urlopen("URL") as url:
	# 		data = json.loads(url.read().decode())
	# 		data = random.choice(data['data'])
	# 		data = data['embed_url']

	# 		if ctx.author.top_role.colour:
	# 			col = ctx.author.top_role.colour
	# 		else:
	# 			col =self.settings.randomColor()
			
	# 		embed=discord.Embed(title="music", color=col)
	# 		embed.set_image(url=data)
	# 		# await ctx.send(embed=embed)
	# 		# await ctx.send(data)

