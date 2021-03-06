import asyncio
import json
import random
import discord
import urllib.request
import requests
import aiohttp
import os
from collections import Counter
from discord.ext import commands

from Utils import Utils

class EventHonk(commands.Cog):
	def __init__(self, bot, settings):
		self.bot = bot
		self.settings = settings
		self.Utils = Utils.Utils()

	@commands.Cog.listener()
	async def on_message(self, message):
		if message.author.id == self.bot.user.id:
			return 	

		if type(message.channel) == discord.DMChannel:
			return

		if self.settings.ServerConfig(message.guild.id, 'HonkEnable') == True:
			if message.channel.id == self.settings.ServerConfig(message.guild.id, 'HonkChannel') or self.settings.ServerConfig(message.guild.id, 'HonkChannel') == 0:
				msgs = message.content
				m = msgs.lower()
				m = m.split()

				# Looks for words 4 letters hnok

				end = 4
				start = 0

				sen = []
				for a in m:
					d = list(a)
					for ass in d:
						sen.append(ass.lower())  	

				while end != len(sen)+1:
					if ("h" in sen[start:end] or "🇭" in sen[start:end]) and ("o" in sen[start:end] or "🇴" in sen[start:end]) and ("n" in sen[start:end] or "🇳" in sen[start:end]) and ("k" in sen[start:end] or "🇰" in sen[start:end]):
						search = random.choice(['honk', 'goose'])
						data = random.choice([self.Utils.ImgurSearch(search), self.Utils.GiphySearch(self.bot.GIPHY_API, search)])

						await message.channel.send(data)

					start += 1
					end += 1

	@commands.command()
	async def enableHonk(self, ctx):
		"""
		Enables Honk API to post images
		"""
		if self.settings.ServerConfig(ctx.guild.id, 'HonkEnable') == True:
			self.settings.ServerConfig(ctx.guild.id, 'HonkEnable', False)
			await ctx.send('Disabling Honk listener')
		else:
			self.settings.ServerConfig(ctx.guild.id, 'HonkEnable', True)			
			await ctx.send('Enabling Honk listener')
	
	@commands.command()
	async def setHonkChannel(self, ctx, name=None):
		"""
		[Channel]
		Adds a dedicated Channel for Honk images
		"""
		if not name: 
			return await ctx.send('No channel entered')
		
		try:
			if int(name) == 0:
				self.settings.ServerConfig(ctx.guild.id, 'HonkChannel', 0)
				return await ctx.send('The No U channel is removed')
		except:
			pass

			ch = self.settings.Get(ctx, 'channel', name)
			if not ch:
				ch = ctx.channel
				
			self.settings.ServerConfig(ctx.guild.id, 'HonkChannel', ch.id)
		await ch.send('The New No U channel to listen on is: {}'.format(ch))

def setup(bot):
	settings = bot.get_cog("Settings")
	bot.add_cog(EventHonk(bot, settings))