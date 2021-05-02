import os
import discord
import tempfile
import shutil
import time
import datetime
from discord.ext import commands
from Scripts import Downloader

# Bot Owner Only

class CogUtils(commands.Cog):
	def __init__(self, bot, settings):
		self.bot = bot
		self.settings = settings
		self.d = Downloader.Downloader()

	def server_owner(ctx):
		return ctx.message.author.id == ctx.guild.owner_id

	@commands.command()
	@commands.is_owner()
	async def addCog(self, ctx):
		"""Upload a File and run this command as the comment only works in DM's"""

		for o in ctx.message.attachments:
			orig_url = o.url	
			file = orig_url.split('/')[len(orig_url.split('/'))-1]
			toLoad = file.replace('.py', '')
			if os.path.exists('Cogs/'+file):
				return await ctx.send('File exists')

			await ctx.send('Adding Cog: **' + toLoad + '**')
			with tempfile.TemporaryDirectory() as tmpdirname:
				self.d.Download(orig_url, tmpdirname)
				if os.path.exists(tmpdirname+'/'+file):
					shutil.move(tmpdirname+'/'+file, 'Cogs')

					time.sleep(0.05)
					self.bot.load_extension('Cogs.'+toLoad)
					await ctx.send('Cog: **' + toLoad + '** has been loaded')

	@commands.command()
	@commands.is_owner()
	async def uploadCog(self, ctx, cog=None):
		"""
		[Cog name] 
		Uploads a Cog
		"""
		if not cog: 
			return await ctx.send(f'You haven\'t specified a Cog name. use `{ctx.prefix}listCog` to list cogs')
		if not cog in self.bot.cogs:
			return await ctx.send('I can not find the Cog:', cog)

		await ctx.send(file=discord.File(fp=f"Cogs/{cog}.py", filename=f'{cog}.py'))

	@commands.command()
	@commands.is_owner()
	async def updateCog(self, ctx):
		"""
		Upload a File and run this command as the comment only works in DM's
		This will make a backup of file before replacement
		"""

		orig_url = ctx.message.attachments[0].url
		file = orig_url.split('/')[len(orig_url.split('/'))-1]
		toLoad = file.replace('.py', '')
		if os.path.exists('Cogs/'+file):
			self.bot.unload_extension('Cogs.'+toLoad)
			time.sleep(0.05)

			Backup = 'Backup'
			if not os.path.exists(Backup):
				os.mkdir(Backup)

			x = datetime.datetime.now()
			f = toLoad+'-'+str(x).replace(':', '!').replace('.', '#')+'.py'
			shutil.move('Cogs/'+file, Backup+'/'+f)
		
		await ctx.send('Adding Cog: ' + toLoad)
		with tempfile.TemporaryDirectory() as tmpdirname:
			self.d.Download(orig_url, tmpdirname)
			if os.path.exists(tmpdirname+'/'+file):
				shutil.move(tmpdirname+'/'+file, 'Cogs')

				time.sleep(0.05)
				self.bot.load_extension('Cogs.'+toLoad)
				await ctx.send('Cog: **' + toLoad + '** has been loaded')

	@commands.command()
	@commands.check(server_owner)
	async def disablecom(self, ctx, add_rem=None, *, cog_com=None):
		"""[add/rem][cog/s]
		Adds or removes command from being used on the server"""
		com = self.settings.ServerConfig(ctx.guild.id, 'DisabledCommands')
		
		PrevCogs = []
		for c in ['Moderation', 'Perms', 'Settings', 'Error', 'Listeners', 'CogLoader']:
			__cog = self.bot.get_cog(c)
			commands = __cog.get_commands()
			comm = [c.name for c in commands]
			for p in comm:
				PrevCogs.append(p)

		

		if add_rem:
			try:	
				cc = cog_com.split(" ")
			except  AttributeError:
				return await ctx.send('Command usage: `{0}{1} add help` or `{0}{1} rem help` '.format(ctx.prefix, ctx.command))

			if add_rem == 'add': # add
				for c in cc:
					if not c in com and not c in PrevCogs:
						com.append(str(c))
				await ctx.send('I have added: %s to list' % cog_com)

			if add_rem == 'rem': # Remove 
				for c in cc:
					if c in com and not c in PrevCogs:
						com.remove(str(c))
				await ctx.send('I have removed: %s from list' % cog_com)

			self.settings.ServerConfig(ctx.guild.id, 'DisabledCommands', com)


		else: # display disabled, cogs and coms
			msg = '**Disabled Cogs and Commands**' # Split into Cogs and Commands
			cogs = [c for c in self.bot.cogs.keys()]
			_cog = ''
			_com = ''
			
			for m in com:
				if m in cogs:
					_cog += '\n - ' + m	
				else:
					_com += '\n - ' + m	

			msg += '\nCogs Disabled:'
			msg += _cog if len(_cog) > 0 else ' None'
			msg += '\nCommands Disabled:'
			msg += _com if len(_com) > 0 else ' None'
			await ctx.send(msg)


def setup(bot):
	settings = bot.get_cog("Settings")
	bot.add_cog(CogUtils(bot, settings))