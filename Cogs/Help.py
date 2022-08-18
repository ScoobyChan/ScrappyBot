import asyncio
import os
import discord
from discord.ext import commands
from collections import Counter

from Utils import Utils

# Need to Show What is needed for Cogs
# show description
# Show if Disabled
# Add Doc code to Commands

# Fix this please

def setup(bot):
	bot.remove_command("help")
	settings = bot.get_cog("Settings")
	bot.add_cog(Help(bot, settings))

class Help(commands.Cog):
	def __init__(self, bot, settings):
		self.bot = bot
		self.settings = settings
		
		self.Utils = Utils.Utils()

	@commands.command()
	async def oldhelp(self, ctx):
		"""Old help before improvement"""
		await ctx.send('Help me :sob:')

	@commands.command()
	async def help(self, ctx, cog_=None):
		"""[cog/command]
		Help command for everything"""
		num = 0
		cogs = [str(c) for c in self.bot.cogs.keys()]
		commands = []
		lennum = len(cogs) - 1

		cogs.sort()
		cogs.remove('Settings')

		for _cogs in cogs:
			_cog = self.bot.get_cog(_cogs)
			for c in _cog.get_commands():
				commands.append(str(c))

		col = ctx.author.top_role.colour or self.settings.randomColor()

		reacts = ['⏮️','◀️','▶️','⏭️']

		msg = await ctx.send('\u200b')
		await asyncio.sleep(0.05)

		if not cog_:
			while True:
				desc = ''
				_cog = self.bot.get_cog(cogs[num])
				# _cog = _cog.sort(reverse=True)
				commands = _cog.get_commands()
				commands.sort()
				if len(commands) > 0:
					for c in commands:
						if c.help:
							desc += '\n**{0}{1}**\n└─ {0}{1} {2}...'.format(self.settings.ServerConfig(ctx.guild.id, 'Prefix'), c, c.help[:15] if c.help else "")
						else:
							print(c, 'add doc code to this command :D')
							desc += '\n**{0}{1}**\n└─ {0}{1}'.format(self.settings.ServerConfig(ctx.guild.id, 'Prefix'), c)
				else:
					desc = 'No commands in module'
				embed = discord.Embed(
					title = 'Help Menu - {}{}'.format(cogs[num], '' if not cogs[num] in self.settings.ServerConfig(ctx.guild.id, 'DisabledCommands') else ' - Disabled by Server Owner'),
					description = desc,
					colour = col
				)
				embed.set_footer(text='Cog Page {}/{}'.format((num + 1), len(cogs)))
				await msg.edit(content=None, embed=embed)

				try:	
					for r in reacts:
						await msg.add_reaction(r)

					def check(reaction: discord.Reaction, adder: discord.User) -> bool:
						return adder == ctx.message.author and reaction.message.id == msg.id

					reaction, adder = await self.bot.wait_for('reaction_add', timeout=30, check=check)
					if reaction.emoji == reacts[0]:
						num = 0

					if reaction.emoji == reacts[1]:
						if not num == 0:
							num -= 1

					if reaction.emoji == reacts[2]:
						if not num == lennum:
							num += 1

					if reaction.emoji == reacts[3]:
						num = lennum

					await msg.remove_reaction(reaction, adder)

				except asyncio.exceptions.TimeoutError:
					break
			
			for r in reacts:
				await msg.remove_reaction(r, self.bot.user)

			return

		# Done
		if cog_ in cogs:
			desc = ''
			_cog = self.bot.get_cog(cog_)
			commands = _cog.get_commands()
			for c in commands:
				# print(c.help)
				desc += '\n**{0}{1}**\n└─ {0}{1} {2}...'.format(self.settings.ServerConfig(ctx.guild.id, 'Prefix'), c, c.help[:15] if c.help else "")

			embed = discord.Embed(
				title = 'Help Menu - Commands for: {}'.format(cog_),
				description = desc,
				colour = col
			)
			
			await ctx.send(embed=embed)

		# Done
		if cog_ in commands:
			for _cogs in cogs:
				_cog = self.bot.get_cog(_cogs)
				for c in _cog.get_commands():
					if str(c) == cog_:
						desc = '**{}{}** {}'.format(self.settings.ServerConfig(ctx.guild.id, 'Prefix'), str(c), c.help)
						embed = discord.Embed(
							title = '{0} Cog - {0}.py'.format(_cogs),
							description = desc,
							colour = col
						)
						
						await ctx.send(embed=embed)
						break

		# Done
		if not cog_ in cogs and not cog_ in commands:
			# print("Can't find item")
			ResCog = self.settings.Search(cog_, cogs)
			ResCom = self.settings.Search(cog_, commands)
			
			dsec = '\n**Possible Cogs**'
			for c in ResCog[:3]:
				dsec += '\n└─ {}'.format(c)

			dsec += '\n**Possible Commands**'
			for c in ResCom[:3]:
				dsec += '\n└─ {}'.format(c)

			embed = discord.Embed(
				title = 'Results',
				description = dsec,
				colour = col
			)
			
			return await ctx.send(embed=embed)

	@commands.command()
	async def listcogs(self, ctx):
		"""Lists the different Cogs"""
		desc = [str(c) for c in self.bot.cogs.keys()]
		desc.remove('Settings')
		desc.sort()

		col = ctx.author.top_role.colour or self.settings.randomColor()

		embed = discord.Embed(
			title = 'Cogs',
			description = desc,
			colour = col
		)	
		await ctx.send(embed=embed)

	@commands.command()
	async def dumphelp(self, ctx):
		"""Puts all the help commands into a text file"""
		_help = []

		cogs = [c for c in self.bot.cogs.keys()]
		cogs.sort()
		cogs.remove('Settings')

		f= open(f"Help.txt","w+")
		for cog_ in cogs:
			_help.append(f"======  {str(cog_)}  ======")
			_cog = self.bot.get_cog(cog_)
			commands = _cog.get_commands()
			for c in commands:
				# _help += 
				# print(str('└─ {0}{1} {2}'.format(self.settings.ServerConfig(ctx.guild.id, 'Prefix'), str(c), c.help)))
				_help.append(str(f' - {self.settings.ServerConfig(ctx.guild.id, "Prefix")}{c}'))
				if c.help:
					_help.append(str(f' --- {c.help}'))

				else:
					_help.append(str(f' --- None'))
			_help.append('\n')

		f.write('\n'.join(_help))		
		f.close()

		await ctx.send(file=discord.File(fp="Help.txt", filename='Help.txt'))

		os.remove('Help.txt')