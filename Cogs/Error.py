import discord
from discord.ext import commands

import traceback
import logging
from datetime import tzinfo, timedelta, datetime, date
import os
import sys

log = '.Error'
if not os.path.exists(log):
	os.mkdir(log)

class Error(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		logging.basicConfig(filename=log+'/error.log', level=logging.CRITICAL, format='%(asctime)s:%(levelname)s:%(message)s')

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

		db_int = self.bot.get_cog("Database_interact")
		if db_int: error_channel = db_int.get_database_item("ErrorChannel")
		if not error_channel: return
		b = self.bot.get_channel(error_channel)

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
		# if isinstance(error, commands.NoEntryPointError):
		# 	if b: return await b.send(error)

		if isinstance(error, commands.CommandInvokeError):
			if 'DiscordException' in str(error):
				return await ctx.send(str(error)[len("Command raised an exception: DiscordException: "):])

			if 'annot send messages' in str(error):
				return await ctx.send('Please enable DM from this server **' + ctx.author.name + '**')
			
			elif "'NoneType' object has no attribute 'send'" in str(error):
				if b:
					return await b.send(embed=embed)
				print(error)
			
			else:
				if b:
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
	
		if not ch: ch = ctx.channel

		db_int = self.bot.get_cog("Database_interact")
		if db_int: 
			db_int.update_database_item("ErrorChannel", ch.id)
			msg = 'Set error channel to: **' + str(ch) + '** in ' + str(ctx.guild)
		else:
			msg = "Unable to update Error Channel"
		await ctx.send(msg)

	@commands.command()
	@commands.is_owner()
	async def testerrorchannel(self, ctx):
		"""Tests the error channel"""
		db_int = self.bot.get_cog("Database_interact")
		if db_int: error_channel = db_int.get_database_item("ErrorChannel")
		if not error_channel: return
		b = self.bot.get_channel(error_channel)
		
		if b:
			await b.send('Test Error channel')
		else:
			await ctx.send('Cant find Error channel')

def setup(bot):
	bot.add_cog(Error(bot))