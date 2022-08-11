# Check in onjoin that if muted keep
import asyncio
import time
import discord
from discord.ext import commands

def setup(bot):
	settings = bot.get_cog("Settings")
	bot.add_cog(Mute(bot, settings))

class Mute(commands.Cog):
	def __init__(self, bot, settings):
		self.bot = bot
		self.settings = settings
		self.mutes = []
		self.mute_loaded = False

	###################
	#  COG LISTENERS  #
	###################

	@commands.Cog.listener()
	async def on_unloaded_extension(self, ext):
		if self.mute_loaded == True:
			if self.bot.debug: print('unloading')
			self.mute_loaded = False

			# Cancel Temproles
			for task in self.mutes:
				if self.bot.debug: print('Removing task')
				task.cancel()

	# This is active
	@commands.Cog.listener()
	async def on_loaded_extension(self, ext):
		# Waits till Bot is ready
		await self.bot.wait_until_ready()
		
		# Stops the loops from activating multiple times
		if self.mute_loaded == False:
			if self.bot.debug: print("Initializing the Mutes")
			if self.bot.debug: print('Cog loaded')
			self.mute_loaded = True
			await self.initialmuteloop()


	###########################
	# FUNCTION SECTION STARTS #
	###########################

	async def MuteEnd(self, guild, role, member, channel, task):
		if role:
			if role in member.roles:
				await member.remove_roles(role)
		else:
			for c in guild.channels:
				if type(c) != discord.CategoryChannel:
					await c.set_permissions(member, overwrite=None)

		if channel:
			text = 'Unmuting **{0}**({0.id})'.format(member)
			embed=discord.Embed(
				title = 'Mute Log',
				description = text,
				color=discord.Color(6208701)
			)
			await channel.send(embed=embed)

		task.cancel()

		if task in self.mutes:
			self.mutes.remove(task)

	async def initialmuteloop(self):
		for guild in self.bot.guilds:
			Users = self.settings.ServerConfig(guild.id, 'MutedUsers')
			for member in Users:
				print('Resuming Mute Time for: {} in guild ID ({})'.format(self.bot.get_user(int(member)), guild))
				self.mutes.append(self.bot.loop.create_task(self.muteloop(guild.id, member)))

	async def muteloop(self, Guild, member):
		task = asyncio.current_task()
		for g in self.bot.guilds:
			if int(g.id)  == int(Guild): guild = g; break

		self.settings.MuteConfig(guild.id, str(member), 'MuteTask', str(task.get_name()))

		# Settings
		_users = self.settings.ServerConfig(guild.id, 'MutedUsers')
		LogChannel = self.settings.ServerConfig(guild.id, 'LogChannel')

		# Fetch users and mute role
		_role = discord.utils.get(guild.roles, id=self.settings.ServerConfig(guild.id, 'MuteRole'))
		_member = discord.utils.get(guild.members, id=int(member)) # User to mute
		_log_channel = discord.utils.get(guild.channels, id=LogChannel)
		_MuteUser = discord.utils.get(guild.channels, id=self.settings.MuteConfig(guild.id, member, 'MuteUser'))

		if _log_channel:
			_time_allocated = self.settings.MuteConfig(guild.id, _member.id, _role.id, 'MuteTime', 0)
			if _MuteUser:
				text = 'Muting **{0}**({0.id}) for {1}\nMuted by: **{2}**({2.id})'.format(_member, _time_allocated, _MuteUser)
			else:
				text = 'Muting **{0}**({0.id}) for {1}'.format(_member, _time_allocated)

			try:	
				embed=discord.Embed(
					title = 'Mute Log',
					description = text,
					color=discord.Color(6208711)
				)
				await _log_channel.send(embed=embed)
			except Exception as e:
				print(e)

		# If muted Add role to user
		if _role:
			# print('Found Role')
			if not _role in _member.roles:
				# print('Add Role')
				await _member.add_roles(_role)
		else:
			overwrite = discord.PermissionOverwrite()
			overwrite.send_messages = False
			overwrite.speak = False
			overwrite.read_messages = True
			for c in guild.channels:
				if type(c) != discord.CategoryChannel:
					await c.set_permissions(member, overwrite=overwrite)

		while True:
			_loop_start_time = int(time.time())
			_init_time = self.settings.MuteConfig(guild.id, str(_member.id), 'MuteAdded')
			_mute_time = self.settings.MuteConfig(guild.id, str(_member.id), 'MuteTime')
			_is_muted = self.settings.MuteConfig(guild.id, _member.id, _role.id, 'IsMuted')

			if _mute_time > 0 or _is_muted == False:	
				if _mute_time <= (_loop_start_time - _init_time) or _is_muted == False:
					# Unmute user
					await self.MuteEnd(guild, _role, _member, _log_channel, task)

					# Remove Muted user
					self.settings.MuteConfig(guild.id, _member.id, _role.id, 'IsMuted', False)
					self.settings.MuteConfig(guild.id, _member.id, passback='del')
					break

				else:
					_time_to_wait = _mute_time - (_loop_start_time - _init_time)
					self.settings.MuteConfig(guild.id, _member.id, 'MuteTime', _time_to_wait)

					# Sleep for x
					await asyncio.sleep(_time_to_wait)
			else:
				await asyncio.sleep(1)
	
	async def _mute(self, ctx, _member, _channel, _guild, _time):
		if not _member:
			return await ctx.send('Can\'t find user {}'.format(_member))

		if _time > 0: _time_conv = self.settings.time_convert(_time)

		# Check if User
		_users = self.settings.ServerConfig(_guild.id, 'MutedUsers')
		if str(_member.id) in _users:
			# increase time if needed
			_init_time = self.settings.MuteConfig(_guild.id, _member.id, 'MuteTime')
			if _init_time == -1: 
				self.settings.MuteConfig(_guild.id, _member.id, 'MuteTime', _time_conv[1])
				await ctx.send('Muting {} for {} by **{}**'.format(_member.name, _time_conv[0], ctx.author.name))
			else:
				_new_time = _init_time + _time_conv[1]
				self.settings.MuteConfig(_guild.id, str(_member.id), 'MuteTime', _new_time)
				await ctx.send('Muting {} for an extra {} by **{}**'.format(_member.name, _time_conv[0], ctx.author.name))
		else:
			self.settings.MuteConfig(_guild.id, _member.id, 'IsMuted', True)
			if _time == -1:	
				# Unlimited Timer
				self.settings.MuteConfig(_guild.id, _member.id, 'MuteTime', -1)
			else:
				# Normal Timer
				if not _time_conv[1] >= 10: 
					return await ctx.send('Time too short')
				
				self.settings.MuteConfig(_guild.id, _member.id, 'MuteTime', _time_conv[1])

			await ctx.send('Muting {} for {} by **{}**'.format(_member.name, _time_conv[0] if _time > 0 else "all eternity", ctx.author.name))
			self.mutes.append(self.bot.loop.create_task(self.muteloop(_guild.id, _member.id)))

	@commands.command()
	async def mute(self, ctx, _user: commands.Greedy[discord.Member] = None, *, _mute_time=-1):
		"""
		[Member][time(e.g. d1 h1 m1 s1 or 11121)]
		Mutes a member for a certain amount of time
		"""
		if not isinstance(_user, list):
			_user = [_user]
		
		guild = ctx.guild
		channel = discord.utils.get(guild.channels, id=self.settings.ServerConfig(guild.id, 'LogChannel'))	
		
		for m in _user:
			await self._mute(ctx, m, channel, guild, _mute_time)
		
	@commands.command()
	async def unmute(self, ctx, _user: commands.Greedy[discord.Member] = None):
		"""[user]
		Unmutes User. 
		"""

		if not isinstance(_user, list):
			_user = [_user]
		
		guild = ctx.guild
		channel = discord.utils.get(guild.channels, id=self.settings.ServerConfig(guild.id, 'LogChannel'))	
		
		for _member in _user:
			role = discord.utils.get(guild.roles, id=self.settings.ServerConfig(guild.id, 'MuteRole'))

			if not _member: await ctx.send('Can\'t find user {}'.format(_member))

			msg = await ctx.send('Unmuting {} by **{}**'.format(_member.name, ctx.author.name))
			# Remove Role/Perms
			await msg.edit(content='Removing Perms/Role')

			# get task:
			task = None
			_task_number = self.settings.MuteConfig(guild.id, _member.id, 'MuteTask')
			for t in self.mutes:
				if t.get_name() == _task_number: task = t

			await self.MuteEnd(guild, role, _member, channel, task)

			# IsMuted to False
			self.settings.MuteConfig(guild.id, _member.id, 'IsMuted', False)

			# Remove from list
			self.settings.MuteConfig(guild.id, _member.id, passback='del')
			
			await msg.edit(content='Unmuted User {}'.format(_member.name))
	
	@commands.command()
	async def muterole(self, ctx):
		"""Displays the mute role"""
		role = discord.utils.get(ctx.guild.roles, id=self.settings.ServerConfig(ctx.guild.id, 'MuteRole'))
		if ctx.author.top_role.colour:
			color = ctx.author.top_role.colour
		else:
			color =self.settings.randomColor()

		embed = discord.Embed(
			title="Current Mute Role",
			description=' - <@&{}>'.format(role.id) if role else 'No Mute Role found',
			colour = color
		)

		await ctx.send(embed=embed)

	@commands.command()
	async def setmuterole(self, ctx, MuteRole: discord.Role=None):
		"""[rolename]
		Sets the mute role with the right permissions too (May need to move it into the right position"""
		color = self.settings.randomColor()

		overwrite = discord.PermissionOverwrite()
		overwrite.send_messages = False
		overwrite.speak = False
		overwrite.read_messages = True

		msg = await ctx.send('Finding Role: **%s**' % MuteRole)
		
		if MuteRole == None:
			self.settings.ServerConfig(ctx.author.id, 'MuteRole', 0)

			embed = discord.Embed(
				title="I have removed the previous Mute role",
				colour = color
			)

			await asyncio.sleep(1)
			return await ctx.send(embed=embed)
		
		if not MuteRole:
			# Creates the role if missing
			await msg.edit(content='Creating Role: **%s**' % MuteRole)
			MuteRole = await ctx.guild.create_role(name=MuteRole, colour=color)

		await asyncio.sleep(1)
		await msg.edit(content='Syncing Role: **%s**' % MuteRole)

		for c in ctx.guild.channels:
			if type(c) != discord.CategoryChannel:
				await c.set_permissions(MuteRole, overwrite=overwrite)

		await asyncio.sleep(1)
		await msg.edit(content='Role: **%s** has synced with the channels' % MuteRole)

		self.settings.ServerConfig(ctx.guild.id, 'MuteRole', MuteRole.id)
		
		embed = discord.Embed(
			title="Current Mute Role",
			description=" - <@&%s>" % MuteRole.id,
			colour = color
		)

		await asyncio.sleep(1)
		await msg.edit(content=None, embed=embed)

	@commands.command()
	async def syncmuterole(self, ctx):
		"""Sync Role and Users to new Channels"""

		overwrite = discord.PermissionOverwrite()
		overwrite.send_messages = False
		overwrite.speak = False
		overwrite.read_messages = True

		guild = ctx.guild
		role = discord.utils.get(ctx.guild.roles, id=self.settings.ServerConfig(guild.id, 'MuteRole'))
		
		if ctx.author.top_role.colour:
			color = ctx.author.top_role.colour
		else:
			color =self.settings.randomColor()

		embed = discord.Embed(
			title="Syncing Mute Role",
			description=' - <@&{}>'.format(role.id) if role else 'No Mute Role found',
			colour = color
		)

		msg = await ctx.send(embed=embed)

		if role:
			for c in ctx.guild.channels:
				if type(c) != discord.CategoryChannel:
					await c.set_permissions(role, overwrite=overwrite)

			embed = discord.Embed(
				title="Synced Mute Role",
				description=' - <@&{}>'.format(role.id),
				colour = color
			)

			await msg.edit(embed=embed)
			
	@commands.command()
	async def desyncmuterole(self, ctx):
		"""Desyncs Roles and Users from Channels"""
		
		guild = ctx.guild
		role = discord.utils.get(guild.roles, id=self.settings.ServerConfig(guild.id, 'MuteRole'))
		print(guild.id)
		print(self.settings.ServerConfig(guild.id, 'MuteRole'))

		if ctx.author.top_role.colour:
			color = ctx.author.top_role.colour
		else:
			color =self.settings.randomColor()

		embed = discord.Embed(
			title="Desyncing Mute Role",
			description=' - <@&{}>'.format(role.id) if role else 'No Mute Role found',
			colour = color
		)

		msg = await ctx.send(embed=embed)

		if role:
			for c in guild.channels:
				if type(c) != discord.CategoryChannel:
					await c.set_permissions(role, overwrite=None)

			embed = discord.Embed(
				title="Desynced Mute Role",
				description=' - <@&{}>'.format(role.id),
				colour = color
			)

			await msg.edit(embed=embed)