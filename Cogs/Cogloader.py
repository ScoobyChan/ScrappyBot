import os
import sys
import datetime
import time
import discord
from discord.ext import commands
import traceback

async def setup(bot: commands.Bot) -> None:
	settings = bot.get_cog("Settings")
	await bot.add_cog(Cogloader(bot, settings))

start_time = time.time()

class Cogloader(commands.Cog):
	def __init__(self, bot, settings):
		self.bot = bot
		self.settings = settings
		self.cog_loaded = []

	def loaded(self):
		print('Loaded {} {}'.format(len(self.bot.cogs), 'Cog' if len(self.bot.cogs) < 2 else 'Cogs'))
		print('Logged in as:{0} (ID: {0.id})\n'.format(self.bot.user))
		print('{}/{}/{}, {}:{}:{}\n'.format(self.bot.res.tm_mday if len(str(self.bot.res.tm_mday)) > 1 else ('0' + str(self.bot.res.tm_mday)), self.bot.res.tm_mon if len(str(self.bot.res.tm_mon)) > 1 else ('0' + str(self.bot.res.tm_mon)), self.bot.res.tm_year, self.bot.res.tm_hour if len(str(self.bot.res.tm_hour)) > 1 else ('0' + str(self.bot.res.tm_hour)), self.bot.res.tm_min if len(str(self.bot.res.tm_min)) > 1 else ('0' + str(self.bot.res.tm_min)), self.bot.res.tm_sec if len(str(self.bot.res.tm_sec)) > 1 else ('0' + str(self.bot.res.tm_sec))))
		print("Invite Link:\nhttps://discordapp.com/oauth2/authorize?client_id={}&scope=bot&permissions=8\n".format(self.bot.user.id))

	async def _load_extension(self, sel_cog=None):
		# Find cogs to load
		directory = "Cogs"
		cog_list = os.listdir(directory)
		for x in ['__pycache__', 'Settings', 'cog_loader', 'Perms']:
			if x in cog_list: cog_list.remove(x)
		
		if sel_cog:
			if not sel_cog in self.cog_loaded:
				cog = '{}.{}'.format(directory, sel_cog)
				try:
					if not self.bot.get_cog(sel_cog):
						await self.bot.load_extension(cog)
						self.bot.dispatch("loaded_extension", self.bot.extensions.get(cog))
				except Exception as error:	
					print('{} cannot be loaded. [{}]'.format(sel_cog, error))
					print(str("".join(traceback.format_exception(type(error), error, error.__traceback__))))

		if os.path.exists('Cogs/Perms.py'):
			try:
				if not self.bot.get_cog("Cogs.Perms"):
					await self.bot.load_extension("Cogs.Perms")

				cog_perm = self.bot.get_cog('Perms')
				# await cog_perm.initiate() set up on cog side

				self.bot.dispatch("loaded_extension", self.bot.extensions.get('Cogs.Perms'))
			except Exception as error:
				print('{} cannot be loaded. [{}]'.format('Perms', error))

		# Load rest of the cogs

		for c in cog_list:
			lname = c.split('.')[0]
			cog = '{}.{}'.format(directory, lname)
			try:
				if not self.bot.get_cog(lname):
					await self.bot.load_extension(cog)
					self.bot.dispatch("loaded_extension", self.bot.extensions.get(cog))

					self.cog_loaded.append(cog)
			except Exception as error:
				print('{} cannot be loaded. [{}]'.format(lname, error))
				print(str("".join(traceback.format_exception(type(error), error, error.__traceback__))))

	async def _unload_extension(self, sel_cog=None):
		directory = "Cogs"

		if sel_cog:
			if not sel_cog in self.cog_loaded:
				cog = '{}.{}'.format(directory, sel_cog)
				try:
					if not self.bot.get_cog(sel_cog):
						self.bot.dispatch("unloaded_extension", self.bot.extensions.get(cog))
						await self.bot.unload_extension(cog)
				except Exception as error:	
					print('{} cannot be unloaded. [{}]'.format(sel_cog, error))
					print(str("".join(traceback.format_exception(type(error), error, error.__traceback__))))

		for c in self.cog_loaded:
			cog = '{}.{}'.format(directory, c)
			try:
				if self.bot.get_cog(c):
					self.bot.dispatch("unloaded_extension", self.bot.extensions.get(cog))
					await self.bot.unload_extension(cog)
			except Exception as error:
				print('{} cannot be unloaded. [{}]'.format(c, error))

	@commands.command(aliases=['r'])
	@commands.is_owner()
	async def reload(self, ctx, args: str = None):
		"""
		reloads bot
		"""
		msg = await ctx.send('Reloading Cogs')

		await self._unload_extension(args)
		await self._load_extension(args)

		await msg.edit(content='Cogs Successfully reloaded')

	@commands.command(aliases=['l'])
	@commands.is_owner()
	async def load(self, ctx, args: str = None):
		"""
		[cog]
		loads a cog or all of them
		"""
		await self._load_extension(args)
		await ctx.send('Cogs Successfully loaded')
		

	@commands.command(aliases=['unl'])
	@commands.is_owner()
	async def unload(self, ctx, args: str = None):
		"""
		[unloads cog]
		"""
		await self._unload_extension(args)
		await ctx.send('Cogs Successfully unloaded')

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

		#  self._load_extension()

		await ctx.send('Cache has been removed')

	@commands.command()
	@commands.is_owner()
	async def Cogloaded(self, ctx):
		"""
		Shows Cogs loaded
		"""
		await ctx.send('{}'.format([str(c) for c in self.bot.cogs.keys()]))

	@commands.command()
	async def uptime(self, ctx):
		"""
		prints uptime of bot
		"""
		current_time = time.time()
		difference = int(round(current_time - start_time))
		text = str(datetime.timedelta(seconds=difference))
		
		col = ctx.author.top_role.colour or self.settings

		embed = discord.Embed(title=text, color=col)
		await ctx.send(embed=embed)