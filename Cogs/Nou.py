import json
import discord
import random
from discord.ext import commands
from collections import Counter
import re

lang = 'Json/Languages.json'

class Nou(commands.Cog):
	# print('Fun Cog Working')
	def __init__(self, bot):
		self.bot = bot
		self.db_int = self.bot.get_cog("Database_interact")

	async def onmessage(self, message):
		if message.author.id == self.bot.user.id:
			return
			
		if type(message.channel) == discord.DMChannel:
			return
		
		nou_enable = self.db_int.get_guild_database_item(message.guild.id, "guild_nou_enable", 0)
		nou_guild = self.db_int.get_guild_database_item(message.guild.id, "guild_nou_channel", 0)

		if nou_enable == 1:
			if message.channel.id == nou_guild or nou_guild == (0 or None):
				msgs = message.content.lower()

				# translator = Translator()
				# tr = translator.translate(msgs, dest='en')
				# with open(lang) as f:
				# 	datastore = json.load(f)

				# m = tr.text
				
				search = re.search("((no|non).(you|u|tu)|(you|u|tu).(no|non))", msgs)
				if search: await message.channel.send("No u")


	@commands.command()
	async def enableNou(self, ctx):
		"""
		Enables Nou reponses
		"""
		if self.db_int:
			guild_nou = self.db_int.get_guild_database_item(ctx.guild.id, "guild_nou_enable", 0)
			if guild_nou == 1:
				self.db_int.update_guild_database_item(ctx.guild.id, "guild_nou_enable", 0)
				await ctx.send('Disabling No u listener')
			else:
				self.db_int.update_guild_database_item(ctx.guild.id, "guild_nou_enable", 1)	
				await ctx.send('Enabling No u listener')
		
		else:
			await ctx.send("Unable to connect to database")
	@commands.command()
	async def setNouChannel(self, ctx, name: discord.channel = None):
		"""
		[channel]
		sets a dedicated No u channel
		"""
		if not name: name = 0

		if int(name) == 0:
			self.db_int.update_guild_database_item(ctx.guild.id, "guild_nou_channel", 0)
			await ctx.send('The No U channel is removed')
		else:	
			self.db_int.update_guild_database_item(ctx.guild.id, 'guild_nou_channel', name.id)
			await ch.send('The New No U channel to listen on is: {}'.format(ch))

def setup(bot):
	bot.add_cog(Nou(bot))