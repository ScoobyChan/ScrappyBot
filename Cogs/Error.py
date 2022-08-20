import discord
from discord.ext import commands

from Utils import Configuration

import traceback
import logging
from datetime import tzinfo, timedelta, datetime, date
import os
import sys

log = 'Error'
if not os.path.exists(log):
	os.mkdir(log)

class Error(commands.Cog):
	def __init__(self, bot, settings):
		self.bot = bot
		self.settings = settings
		logging.basicConfig(filename=log+'/error.log', level=logging.CRITICAL, format='%(asctime)s:%(levelname)s:%(message)s')
		self.Conf = Configuration.Configuration(bot)

	@commands.Cog.listener()
	async def on_command_error(self, ctx, error):
		com = str(ctx.prefix)+str(ctx.command)
		logging.critical('#'*26)
		logging.critical('Error: ')
		logging.critical(str(error))
		logging.critical(str(error.__traceback__))
		logging.critical(str("".join(traceback.format_exception(type(error), error, error.__traceback__))))
		logging.critical('#'*26)

		embed = discord.Embed(
			title='ERROR',
			description = str(error),
			colour = discord.Color.red()
		)

		if isinstance(error, commands.DisabledCommand):
			return await ctx.send(error)
		if isinstance(error, commands.PrivateMessageOnly):
			return await ctx.send('**'+com+'** can only be used in DM')
		if isinstance(error, commands.NoPrivateMessage):
			return await ctx.send('**'+com+'** can only be used in Guild')
		if isinstance(error, commands.CheckFailure):
			return await ctx.send(str(error))
		if isinstance(error, commands.NSFWChannelRequired):
			return await ctx.send(str(error))
		if isinstance(error, commands.NotOwner):
			return await ctx.send(str(error))
		if isinstance(error, commands.NoEntryPointError):
			b = self.bot.get_channel(self.settings.BotConfig('ErrorChannel'))
			if b:
				return await b.send(error)

		if isinstance(error, commands.CommandInvokeError):
			if 'DiscordException' in str(error):
				return await ctx.send(str(error)[len("Command raised an exception: DiscordException: "):])

			if 'annot send messages' in str(error):
				return await ctx.send('Please enable DM from this server **' + ctx.author.name + '**')
			
			elif "'NoneType' object has no attribute 'send'" in str(error):
				b = self.bot.get_channel(self.settings.BotConfig('ErrorChannel'))
				if b:
					return await b.send(embed=embed)
				print(error)
			
			else:
				b = self.bot.get_channel(self.settings.BotConfig('ErrorChannel'))
				if b:
					return await b.send(embed=embed)
				else:
					embed = discord.Embed(
						title='ERROR: {}'.format(error),
						description = str("".join(traceback.format_exception(type(error), error, error.__traceback__))),
						colour = discord.Color.red()
					)
					return await b.send(embed=embed)

		if "is not found" in str(error) and "command" in str(error).lower():
			return # await ctx.send('No Command found')

		if "argument that is missing" in str(error):
			h = None
			_cogs = ctx.cog
			_cog = self.bot.get_cog(_cogs)
			for c in _cog.get_commands():
				if str(c) == ctx.command:
					h = c
					
			embed = discord.Embed(
				title='Missing argument for command',
				description = h.help if h else None,
				colour = discord.Color.red()
			)
			await ctx.send(embed=embed)


	@commands.command()
	@commands.is_owner()
	async def seterrorchannel(self, ctx, ch: discord.TextChannel=None):
		"""
		[channel]
		sets the error channel
		"""			
	
		if not ch:
			ch = ctx.channel

		self.settings.BotConfig('ErrorChannel', ch.id)

		await ctx.send('Set error channel to: **' + str(ch) + '** in ' + str(ctx.guild))

	@commands.command()
	@commands.is_owner()
	async def testerrorchannel(self, ctx):
		"""Tests the error channel"""

		b = self.bot.get_channel(self.settings.BotConfig('ErrorChannel'))
		if b:
			await b.send('Test Error channel')
		else:
			await ctx.send('Cant find Error channel')




def setup(bot):
	settings = bot.get_cog("Settings")
	bot.add_cog(Error(bot, settings))