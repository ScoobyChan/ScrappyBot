import random
import re
import discord
from collections import Counter
from discord.ext import commands
from Utils import Utils

class EventHonk(commands.Cog):
	def __init__(self, bot, settings):
		self.bot = bot
		self.settings = settings
		self.Utils = Utils.Utils()

	async def onmessage(self, message):
		if message.author.id == self.bot.user.id:
			return 	

		if type(message.channel) == discord.DMChannel:
			return
		
		check_message = message.content
		pattern = r'\b[Hh][Oo][Nn][Kk]+[a-zA-Z]*\b'
		matches = re.findall(pattern, check_message)

		if len(matches) != 0:
			search = random.choice(['canadian goose', 'goose'])
			data = random.choice([self.Utils.ImgurSearch(search), self.Utils.TenorSearch(search), self.Utils.GiphySearch(search)])
			print(data)
			await message.channel.send(data)

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

async def setup(bot: commands.Bot) -> None:
	settings = bot.get_cog("Settings")
	await bot.add_cog(EventHonk(bot, settings))