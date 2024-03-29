import random
import discord
import requests
from discord.ext import commands
import re
import os

from Utils import Utils

class Honk(commands.Cog):
	def __init__(self, bot, settings):
		self.bot = bot
		self.settings = settings
		self.Utils = Utils.Utils()

	async def onmessage(self, message):
		if message.author.bot:
			return 	

		if type(message.channel) == discord.DMChannel:
			return

		if self.settings.ServerConfig(message.guild.id, 'HonkEnable') == True:
			if message.channel.id == self.settings.ServerConfig(message.guild.id, 'HonkChannel') or self.settings.ServerConfig(message.guild.id, 'HonkChannel') == 0:
				msgs = message.content
				
				search_result = re.search("(honk|h.o.n.k|knoh|k.n.o.h)", msgs)

				if search_result:
					search = random.choice(['honk', 'goose'])
					data = self.Utils.ImgurSearch(search)

					img_data = requests.get(data).content

					file = data.split('/')[len(data.split('/')) - 1]

					with open('images/'+file, 'wb') as handler:
						handler.write(img_data)

					_file = discord.File('images/'+file, filename=file)
					await message.channel.send(file=_file)
					os.remove('images/'+file)


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
	bot.add_cog(Honk(bot, settings))