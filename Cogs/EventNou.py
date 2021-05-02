import json
import discord
import random
from discord.ext import commands
from collections import Counter
from googletrans import Translator

lang = 'Json/Languages.json'

class EventNou(commands.Cog):
	# print('Fun Cog Working')
	def __init__(self, bot, settings):
		self.bot = bot
		self.settings =settings

	@commands.Cog.listener()
	async def on_message(self, message):
		if message.author.id == self.bot.user.id:
			return
			
		if type(message.channel) == discord.DMChannel:
			return
			
		if self.settings.ServerConfig(message.guild.id, 'NouEnable') == True:
			if message.channel.id == self.settings.ServerConfig(message.guild.id, 'NouChannel') or self.settings.ServerConfig(message.guild.id, 'NouChannel') == 0:
				msgs = message.content
				msgs = msgs.lower()

				# translator = Translator()
				# tr = translator.translate(msgs, dest='en')
				# with open(lang) as f:
				# 	datastore = json.load(f)

				# m = tr.text
				m = msgs.split()
				


				sen = []
				for a in m:
					d = list(a)
					for ass in d:
						sen.append(ass.lower())  		

				start = 0
				end = 3	

				while end != len(sen)+1:			
					if ("u" in sen[start:end] or "🇺" in sen[start:end]) and ("o" in sen[start:end] or "🇴" in sen[start:end]) and ("n" in sen[start:end] or "🇳" in sen[start:end]):
						await message.channel.send("No u")
						break

					start += 1
					end += 1


	@commands.command()
	async def enableNou(self, ctx):
		"""
		Enables Nou reponses
		"""
		if self.settings.ServerConfig(ctx.guild.id, 'NouEnable') == True:
			self.settings.ServerConfig(ctx.guild.id, 'NouEnable', False)
			await ctx.send('Disabling No u listener')
		else:
			self.settings.ServerConfig(ctx.guild.id, 'NouEnable', True)		
			await ctx.send('Enabling No u listener')

	@commands.command()
	async def setNouChannel(self, ctx, name=None):
		"""
		[channel]
		sets a dedicated No u channel
		"""
		if not name: 
			return await ctx.send('No channel entered')

		try:
			if int(name) == 0:
				self.settings.ServerConfig(ctx.guild.id, 'NouChannel', 0)
				return await ctx.send('The No U channel is removed')
		except:
			pass

			ch = self.settings.Get(ctx, 'channel', name)
			if not ch:
				ch = ctx.channel
			
			self.settings.ServerConfig(ctx.guild.id, 'NouChannel', ch.id)
		await ch.send('The New No U channel to listen on is: {}'.format(ch))

def setup(bot):
	settings = bot.get_cog("Settings")
	bot.add_cog(EventNou(bot, settings))