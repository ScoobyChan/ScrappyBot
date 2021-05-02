# This Module is for loading and managing the Cogs
# Cog loaded progress bar
import tempfile
import asyncio
import os
import sys
import datetime
import time
import json
import shutil
import discord
from discord.ext import commands

from Utils import Utils

def setup(bot):
	bot.add_cog(CogLoader(bot))

start_time = time.time()

class CogLoader(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.Utils = Utils.Utils()

	def _load_extension(self):
		print('Loading Cogs')
		Directory = 'Cogs'
		cogDir = os.listdir(Directory)
		if '__pycache__' in cogDir:
			cogDir.remove('__pycache__')
		self.CogsToLoad = []

		# Load Perms first :D
		if os.path.exists('Cogs/Perms.py'):
			try:
				if not self.bot.get_cog("Cogs.Perms"):
					self.bot.load_extension("Cogs.Perms")

				self.bot.botadmin = []
				self.bot.admin = []
				self.bot.server_owner = []
				self.bot.admin_role = []

				self.bot.kic_ban = []

				self.bot.nsfw = []

				self.bot.dispatch("loaded_extension", self.bot.extensions.get('Cogs.Perms'))
			except Exception as error:
				print('{} cannot be loaded. [{}]'.format('Perms', error))

		dirs = []
		for direct in cogDir:
			if os.path.isdir(Directory+'/'+direct):
				dirs.append([Directory, direct])

			if os.path.isfile(Directory+'/'+direct):
				if not direct == '__pycache__':
					d = [Directory, direct]
					self.CogsToLoad.append('.'.join(d)[:len('.'.join(d))-3])
		
		
		if 'Cogs.CogLoader' in self.CogsToLoad:
			self.CogsToLoad.remove('Cogs.CogLoader')

		if 'Cogs.Settings' in self.CogsToLoad:
			self.CogsToLoad.remove('Cogs.Settings')

		for d in dirs:
			for x in os.listdir('/'.join(d)):
				if not x == '__pycache__':
					d.append(x)

					# print("Cog to load: {}".format('.'.join(d)[:len('.'.join(d))-3]))
					# print("File to load: {}".format('/'.join(d)))
					# print("\n")

					self.CogsToLoad.append('.'.join(d)[:len('.'.join(d))-3])

					d.remove(x)

		cog_counter = 1 
		for cog in self.CogsToLoad:
			try:
				lname = cog.split('.')[len(cog.split('.'))-1]
				if not self.bot.get_cog(lname):
					self.bot.load_extension(cog)
					self.bot.dispatch("loaded_extension", self.bot.extensions.get(cog))
			except Exception as error:
				print('{} cannot be loaded. [{}]'.format(lname, error))
			print("Loaded " + self.Utils.progressbar(cog_counter/len(self.CogsToLoad)))
			cog_counter += 1

	def _unload_extension(self):
		print('Unloading Cogs')

		cog_counter = 1
		for cog in self.CogsToLoad:
			try:
				uname = cog.split('.')[len(cog.split('.'))-1]
				if self.bot.get_cog(uname):
					self.bot.dispatch("unloaded_extension", self.bot.extensions.get(cog))
					self.bot.unload_extension(cog)
					print("Unloaded " + self.Utils.progressbar(cog_counter/len(self.CogsToLoad)))
			except Exception as error:
				print('{} cannot be unloaded. [{}]'.format(uname, error))

			# break
			cog_counter += 1

		if self.bot.get_cog("Cogs.Perms"):
			self.bot.unload_extension("Cogs.Perms")

		print('')

	def loaded(self):
		self.Utils.clear()
		self.Utils.title('%s Online' % self.bot.user.name)
		print('Total Loaded {} {}'.format(len(self.bot.cogs), 'Cog' if len(self.bot.cogs) < 2 else 'Cogs'))
		print("Main Cogs: {}".format(len(os.listdir('Cogs')) - 1))
		for d in os.listdir('Cogs'):
			if not d == '__pycache__' and os.path.isdir("Cogs/"+d):
				print("Folder:", d, "{}".format(len(os.listdir("Cogs/"+d)) - 1))

		print('Logged in as:{0} (ID: {0.id})\n'.format(self.bot.user))
		print('{}/{}/{}, {}:{}:{}\n'.format(self.bot.res.tm_mday if len(str(self.bot.res.tm_mday)) > 1 else ('0' + str(self.bot.res.tm_mday)), self.bot.res.tm_mon if len(str(self.bot.res.tm_mon)) > 1 else ('0' + str(self.bot.res.tm_mon)), self.bot.res.tm_year, self.bot.res.tm_hour if len(str(self.bot.res.tm_hour)) > 1 else ('0' + str(self.bot.res.tm_hour)), self.bot.res.tm_min if len(str(self.bot.res.tm_min)) > 1 else ('0' + str(self.bot.res.tm_min)), self.bot.res.tm_sec if len(str(self.bot.res.tm_sec)) > 1 else ('0' + str(self.bot.res.tm_sec))))
		print("Invite Link:\nhttps://discordapp.com/oauth2/authorize?client_id={}&scope=bot&permissions=8\n".format(self.bot.user.id))
	
	def _update(self):
		with tempfile.TemporaryDirectory() as tmpdirname:
			if not os.path.exists('Temp'):
				os.mkdir('Temp')
			else:
				shutil.move('Temp/', tmpdirname)
				os.mkdir('Temp')

			os.chdir('Temp')
			os.system(f'git clone {self.bot.repo}')
			os.chdir('../')

			if not os.path.exists('Backup'):
				os.mkdir('Backup')

			if len(os.listdir('Backup')) > 9:
				shutil.move(f"Backup/{os.listdir('Backup')[0]}", tmpdirname)

			# make backup
			date = time.localtime()
			dateform = f"{date.tm_mday}-{date.tm_mon}-{date.tm_year}----{date.tm_hour}-{date.tm_min}-{date.tm_sec}"
			if os.path.exists('Cogs/'):
				# shutil.copytree('Cogs/', f'Backup/{dateform}/Cogs/') 
				shutil.move('Cogs/', f'Backup/{dateform}/Cogs/') 

			for o in os.listdir('Temp/'):
				shutil.move(f'Temp/{o}/Cogs', './')

			# shutil.rmtree('Temp')

	@commands.command()
	async def uptime(self, ctx):
		"""
		prints uptime of bot
		"""
		current_time = time.time()
		difference = int(round(current_time - start_time))
		text = str(datetime.timedelta(seconds=difference))
		
		
		col = ctx.author.top_role.colour
		embed = self.Utils.embed({"title":text, "color":col})		
		await ctx.send(embed=embed)

	@commands.command(aliases=['r'])
	@commands.is_owner()
	async def reload(self, ctx):
		"""
		reloads bot
		"""
		msg = await ctx.send('Reloading Cogs')

		self._unload_extension()
		self._load_extension()

		# input()
		self.loaded()

		await msg.edit(content='Cogs Successfully reloaded')

	@commands.command(aliases=['l'])
	@commands.is_owner()
	async def load(self, ctx, args: str):
		"""
		[cog]
		loads a cog or all of them
		"""
		if not args:
			self._load_extension()
			await ctx.send('Cogs Successfully loaded')
		else:
			try:
				self.bot.load_extension('Cogs.'+args)
				await ctx.send('Cogs Successfully loaded')
			except:
				print('{} can not be found or loaded'.format(args))
				await ctx.send('Cogs was not Successful')	

	@commands.command(aliases=['unl'])
	@commands.is_owner()
	async def unload(self, ctx, args: str):
		"""
		[unloads cog]
		"""
		if not args:
			self._unload_extension()
			await ctx.send('Cogs Successfully unloaded')
		else:
			try:
				self.bot.unload_extension('Cogs.'+args)
				await ctx.send('Cogs Successfully unloaded')
			except:
				print('{} can not be found or loaded'.format(args))
				await ctx.send('Cogs was not Successful')

	@commands.command(aliases=['cc'])
	@commands.is_owner()
	async def clearCon(self, ctx):
		"""
		clears the console
		"""
		await ctx.message.delete()
		if not 'win' in sys.platform:
			os.system('clear')
		else:
			os.system('cls')

	@commands.command()
	@commands.is_owner()
	async def ClearCache(self, ctx):
		"""
		Clears the Cache
		"""
		self._unload_extension()
		for o in os.listdir('Cogs/__pycache__'):
			if not o.startswith('CogLoader') and not o.startswith('Settings') and not o.startswith('BotControl'):
				os.remove('Cogs/__pycache__/'+o)

		self._load_extension()

		await ctx.send('Cache has been removed')

	@commands.command()
	@commands.is_owner()
	async def Cogloaded(self, ctx):
		"""
		Shows Cogs loaded
		"""
		await ctx.send('{}'.format([str(c) for c in self.bot.cogs.keys()]))

	@commands.command()
	async def update(self, ctx):
		"""Downloads the latest and updates the bot from the Repo"""
		msg = await ctx.send("Updating Cogs please wait...")

		self._update()