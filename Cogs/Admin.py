import random
import asyncio
import time
import discord
from discord.ext import commands

def setup(bot):
	settings = bot.get_cog("Settings")
	bot.add_cog(Admin(bot, settings))

class Admin(commands.Cog):
	def __init__(self, bot, settings):
		self.bot = bot
		self.settings = settings
		self.tempbans = []
		self.temp_admin_loaded = False

		if self.bot.get_cog('Perms'):
			self.bot.kic_ban.append('ban')
			self.bot.kic_ban.append('kick')
			self.bot.kic_ban.append('unban')
	
	###################
	#  COG LISTENERS  #
	###################

	@commands.Cog.listener()
	async def on_unloaded_extension(self, ext):
		if self.temp_admin_loaded == True:
			if self.bot.debug: print('unloading')
			self.temp_admin_loaded = False

			# Cancel Temproles
			for task in self.tempbans:
				if self.bot.debug: print('Removing task')
				task.cancel()

	@commands.Cog.listener()
	async def on_loaded_extension(self, ext):
		# Waits till Bot is ready
		await self.bot.wait_until_ready()

		# Stops the loops from activating multiple times
		if self.temp_admin_loaded == False:
			if self.bot.debug: print("Initializing the Mutes")
			if self.bot.debug: print('Cog loaded')
			self.temp_admin_loaded = True
			await self.initialtempban()

	###########################
	# FUNCTION SECTION STARTS #
	###########################

	async def initialtempban(self):
		for guild in self.bot.guilds:
			Users = self.settings.ServerConfig(guild.id, 'TempBan')
			for member in Users:
				print('Resuming Temp Ban Time for: {} in guild ID ({})'.format(self.bot.get_user(int(member)), guild))
				self.tempbans.append(self.bot.loop.create_task(self.banloop(guild, member)))

	async def TempBanEnd(self, guild, member, channel, task):
		bans = [b.user.id for b in await guild.bans()]
		if member.id in bans:
			await guild.unban(member)

		if channel:
			text = 'Unbanning **{0}**({0.id})'.format(member)
			embed=discord.Embed(
				title = 'Mute Log',
				description = text,
				color=discord.Color(6208701)
			)
			await channel.send(embed=embed)
		
		task.cancel()

		if task in self.tempbans:
			self.tempbans.remove(task)

	async def banloop(self, guild, member):
		task = asyncio.Task.current_task()

		# print('Mute Loop')
		for g in self.bot.guilds:
			if int(g.id)  == int(guild):
				guild = g
				break

		self.settings.BanConfig(guild.id, str(member), 'Task', str(task.get_name()))

		# Settings
		# _users = self.settings.ServerConfig(guild.id, 'TempBan')
		
		LogChannel = self.settings.ServerConfig(guild.id, 'LogChannel')

		# Fetch users and mute role
		_member = discord.utils.get(guild.members, id=int(member)) # User to mute
		_log_channel = discord.utils.get(guild.channels, id=LogChannel)
		_BanUser = discord.utils.get(guild.channels, id=self.settings.BanConfig(guild.id, member, 'BanUser'))
		
		if _log_channel:
			_time_allocated = self.settings.BanConfig(guild.id, _member.id, 'bantime', 0)
			if _BanUser:
				text = 'Banning **{0}**({0.id}) for {1}\nBanned by: **{2}**({2.id})'.format(_member, _time_allocated, _BanUser)
			else:
				text = 'Banning **{0}**({0.id}) for {1}'.format(_member, _time_allocated)

			try:	
				embed=discord.Embed(
					title = 'Mute Log',
					description = text,
					color=discord.Color(6208711)
				)
				await _log_channel.send(embed=embed)
			except Exception as e:
				print(e)

		# get users ban time
		
		while True:
			_loop_start_time = int(time.time())
			_init_time = self.settings.BanConfig(guild.id, str(_member.id), 'bantimeadded')
			_ban_time = self.settings.BanConfig(guild.id, str(_member.id), 'bantime')
			_is_banned = self.settings.BanConfig(guild.id, _member.id, 'banned')

			if _ban_time > 0 or _is_banned == False:
				if _ban_time <= (_loop_start_time - _init_time) or _is_banned == False:
					await self.TempBanEnd(guild, _member, _log_channel, task)
					self.settings.BanConfig(guild.id, _member.id, 'banned', False)
					self.settings.BanConfig(guild.id, _member.id, passback='del')
					break

				else:
					_time_to_wait = _ban_time - (_loop_start_time - _init_time)
					self.settings.BanConfig(guild.id, _member.id, 'bantime', _time_to_wait)

					await asyncio.sleep(_time_to_wait)
			else:
				await asyncio.sleep(1)

	##########################
	##     COG COMMANDS     ##
	##########################

	async def onmemberjoin(self, message):
		_banned = self.settings.BanConfig(message.guild, message.member, 'banned')
		
		if message.author.id == self.bot.user.id:
			return 	

		if _banned: await message.guild.kick(message.author, reason='User has been temp kicked')

	@commands.command()
	async def kick(self, ctx, _user: commands.Greedy[discord.Member] = None, *, reason=None):
		"""
		[user] [reason]
		This is used to kick users
		"""
		if not isinstance(_user, list):
			_user = [_user]

		msg = ''
		for u in _user:
			if u.id == self.bot.user.id:
				return await ctx.send('You can not ban me I am superior')

			if self.settings.Get(ctx, 'admin', user) == None or self.settings.Get(ctx, 'moderator', user) == None:
				return await ctx.send('you can not ban other moderators')

			if ctx.guild.owner.id == u.id: return await ctx.send('You cannot kick the server owner')
			if self.bot.user.id == u.id: return await ctx.send('You cannot kick the bot')
			if ctx.author.id == u.id: return await ctx.send('You cannot kick yourself')
			await ctx.message.delete()
			con = random.randint(1000, 9999)
			text = f'**Admin Kick**\n{str(u)} ({str(u.id)})\n```\n{reason}\n```\nConfirm Number:\n`{str(con)}`'
			embed = discord.Embed(
				description = text,
				colour = 0x32a8a6
			)
			msg = await ctx.send(embed=embed)
			user = ctx.message.author
			channel = ctx.message.channel
			asyncio.sleep(0.05)

			def check(m):
				return m.content == str(con) and m.channel == channel and m.author == user

			try:
				t = await self.bot.wait_for('message', timeout=10, check=check)
			except asyncio.exceptions.TimeoutError:
				await msg.delete()
				await ctx.send('Kick Attempt of **' + str(u.name) + '** cancelled')
				return

			msg += u.name + '\n'

		await msg.delete()
		await t.delete()
		await ctx.send('`I have kicked: ' + msg + '`')
		await ctx.guild.kick(u, reason=reason)

	@commands.command()
	async def tempkick(self, ctx, _user: commands.Greedy[discord.Member] = None, *, reason=None, kick_time=None):
		"""
		[user] [reason] 
		This is used to kick users
		"""
		if not isinstance(_user, list):
			_user = [_user]

		msg = ''
		for u in _user:
			if u.id == self.bot.user.id:
				return await ctx.send('You can not ban me I am superior')

			if self.settings.Get(ctx, 'admin', user) == None or self.settings.Get(ctx, 'moderator', user) == None:
				return await ctx.send('you can not ban other moderators')

			if ctx.guild.owner.id == u.id: return await ctx.send('You cannot kick the server owner')
			if self.bot.user.id == u.id: return await ctx.send('You cannot kick the bot')
			if ctx.author.id == u.id: return await ctx.send('You cannot kick yourself')
			await ctx.message.delete()
			con = random.randint(1000, 9999)
			text = f'**Admin Kick**\n{str(u)} ({str(u.id)})\n```\n{reason}\n```\nConfirm Number:\n`{str(con)}`'
			embed = discord.Embed(
				description = text,
				colour = 0x32a8a6
			)
			msg = await ctx.send(embed=embed)
			user = ctx.message.author
			channel = ctx.message.channel
			asyncio.sleep(0.05)

			def check(m):
				return m.content == str(con) and m.channel == channel and m.author == user

			try:
				t = await self.bot.wait_for('message', timeout=10, check=check)
			except asyncio.exceptions.TimeoutError:
				await msg.delete()
				await ctx.send('Kick Attempt of **' + str(u.name) + '** cancelled')
				return

			msg += u.name + '\n'

			_time_count, _time_text = self.settings.Time(kick_time)

			if _time_count:
				_users = self.settings.ServerConfig(ctx.guild.id, 'TempBan')
				if str(u.id) in _users:
					self.settings.BanConfig(ctx.guild.id, str(u.id), 'bantime', (self.settings.BanConfig(ctx.guild.id, str(u.id), 'bantime') + kick_time))
				else:
					self.settings.newBanConfig(ctx.guild.id, u.id)
					_time = self.settings.Time(kick_time)
					self.settings.BanConfig(ctx.guild, user, 'bantime', _time)
					self.tempbans.append(self.bot.loop.create_task(self.banloop(ctx.guild.id, u)))


		await msg.delete()
		await t.delete()
		await ctx.send('`I have kicked: ' + msg + '`')
		await ctx.guild.kick(u, reason=reason)

	@commands.command()
	async def ban(self, ctx, _user: commands.Greedy[discord.Member] = None, reason=None, ban_time=None):
		"""
		[users] [reason] [time/optional]
		This is used to ban users with the ban hammer
		"""

		if not isinstance(_user, list):
			_user = [_user]

		msg = ''
		for u in _user:
			if u.id == self.bot.user.id:
				return await ctx.send('You can not ban me I am superior')

			if self.settings.Get(ctx, 'admin', user) == None or self.settings.Get(ctx, 'moderator', user) == None:
				return await ctx.send('you can not ban other moderators')

			if ctx.guild.owner.id == u.id: return await ctx.send('You cannot ban the server owner')
			if self.bot.user.id == u.id: return await ctx.send('You cannot ban the bot')
			if ctx.author.id == u.id: return await ctx.send('You cannot kick yourself')
			await ctx.message.delete()
			con = random.randint(1000, 9999)
			text = f'**Admin Ban**\n{str(u)} ({str(u.id)})\n```\n{reason}\n```\nConfirm Number:\n`{str(con)}`'
			embed = discord.Embed(
				description = text,
				colour = 0x32a8a6
			)
			msg = await ctx.send(embed=embed)
			user = ctx.message.author
			channel = ctx.message.channel
			asyncio.sleep(0.05)

			def check(m):
				return m.content == str(con) and m.channel == channel and m.author == user

			try:
				t = await self.bot.wait_for('message', timeout=10, check=check)
			except asyncio.exceptions.TimeoutError:
				await msg.delete()
				await ctx.send('Ban Attempt of **' + str(u.name) + '** cancelled')
				return

			await msg.delete()
			await t.delete()

		await ctx.send(f'`I have banned: {msg}`') # Add time
		await ctx.guild.ban(u, reason=reason)

	@commands.command()
	async def tempban(self, ctx, _user: commands.Greedy[discord.Member] = None, reason=None, ban_time=None):
		"""
		[users] [reason] [time/optional]
		This is used to ban users with the ban hammer
		"""

		# Rebuidl this to use discord.Members multiples
			
		if not isinstance(_user, list):
			_user = [_user]

		msg = ''
		for u in _user:
			if u.id == self.bot.user.id:
				return await ctx.send('You can not ban me I am superior')

			if self.settings.Get(ctx, 'admin', user) == None or self.settings.Get(ctx, 'moderator', user) == None:
				return await ctx.send('you can not ban other moderators')

			if ctx.guild.owner.id == u.id: return await ctx.send('You cannot ban the server owner')
			if self.bot.user.id == u.id: return await ctx.send('You cannot ban the bot')
			if ctx.author.id == u.id: return await ctx.send('You cannot kick yourself')
			await ctx.message.delete()
			con = random.randint(1000, 9999)
			text = f'**Admin Ban**\n{str(u)} ({str(u.id)})\n```\n{reason}\n```\nConfirm Number:\n`{str(con)}`'
			embed = discord.Embed(
				description = text,
				colour = 0x32a8a6
			)
			msg = await ctx.send(embed=embed)
			user = ctx.message.author
			channel = ctx.message.channel
			asyncio.sleep(0.05)

			def check(m):
				return m.content == str(con) and m.channel == channel and m.author == user

			try:
				t = await self.bot.wait_for('message', timeout=10, check=check)
			except asyncio.exceptions.TimeoutError:
				await msg.delete()
				await ctx.send('Ban Attempt of **' + str(u.name) + '** cancelled')
				return

			await msg.delete()
			await t.delete()

			_time_count, _time_text = self.settings.Time(ban_time)

			if _time_count:
				_users = self.settings.ServerConfig(ctx.guild.id, 'TempBan')
				if str(u.id) in _users:
					self.settings.BanConfig(ctx.guild.id, str(u.id), 'bantime', (self.settings.BanConfig(ctx.guild.id, str(u.id), 'bantime') + ban_time))
				else:
					self.settings.newBanConfig(ctx.guild.id, u.id)
					_time = self.settings.Time(ban_time)
					self.settings.BanConfig(ctx.guild, user, 'bantime', _time)
					self.tempbans.append(self.bot.loop.create_task(self.banloop(ctx.guild.id, u)))

		await ctx.send(f'`I have banned: {msg}` For {_time_text}') # Add time
		await ctx.guild.ban(u, reason=reason, delete_message_days=10)

	@commands.command()
	async def unban(self, ctx, userID: int=None, reason=None):
		"""
		[user ID] [reason]
		used to unban members
		"""
		# Get ban list and to check user is in bans
		u = await self.bot.fetch_user(userID)
		await ctx.message.delete()
		con = random.randint(1000, 9999)
		text = f'**Admin unBan**\n{str(u)} ({str(u.id)})\n```\n{reason}\n```\nConfirm Number:\n`{str(con)}`'
		embed = discord.Embed(
			description = text,
			colour = 0x32a8a6
		)
		msg = await ctx.send(embed=embed)
		user = ctx.message.author
		channel = ctx.message.channel
		asyncio.sleep(0.05)

		def check(m):
			return m.content == str(con) and m.channel == channel and m.author == user

		try:
			t = await self.bot.wait_for('message', timeout=10, check=check)
		except asyncio.exceptions.TimeoutError:
			await msg.delete()
			await ctx.send('unBan Attempt of **' + str(u.name) + '** cancelled')
			return

		await msg.delete()
		await t.delete()

		bans = await ctx.guild.bans()
		if u in bans: 
			await ctx.guild.unban(u, reason=reason)
			await ctx.send('`I have unbanned: ' + u.name + '`')

		self.settings.BanConfig(ctx.guild.id, str(u.id), 'banned', False)

	@commands.command()
	async def bans(self, ctx):
		""""Lists all bans in server"""
		bans = await ctx.guild.bans()
		fuz = self.bot.get_cog('FuzzySearch')
		if fuz: await fuz.fuzList(ctx, bans, 'Server Bans', max_num = 10)