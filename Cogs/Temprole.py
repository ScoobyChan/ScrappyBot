import asyncio
import time
import discord
from discord.ext import commands

def setup(bot):
	settings = bot.get_cog("Settings")
	bot.add_cog(Temprole(bot, settings))

# To do
# channel log

class Temprole(commands.Cog):
	def __init__(self, bot, settings):
		self.bot = bot
		self.settings = settings
		self.temps = []
		self.temp_loaded = False

	###################
	#  COG LISTENERS  #
	###################

	@commands.Cog.listener()
	async def on_unloaded_extension(self, ext):
		if self.temp_loaded == True:
			if self.bot.debug: print('unloading')
			self.temp_loaded = False

			# Cancel Temproles
			for task in self.temps:
				if self.bot.debug: print('Removing task')
				task.cancel()

	@commands.Cog.listener()
	async def on_loaded_extension(self, ext):
		# Waits till Bot is ready
		await self.bot.wait_until_ready()
		
		# Stops the loops from activating multiple times
		if self.temp_loaded == False:
			if self.bot.debug: print("Initializing the Temp roles")	
			if self.bot.debug: print('Cog loaded')
			self.temp_loaded = True
			await self.initialtemploop()

	###########################
	# FUNCTION SECTION STARTS #
	###########################

	async def TempEnd(self, guild, role, member, channel, task):
		if role:
			if self.bot.debug: print('Found Role')
			if role in member.roles:
				if self.bot.debug: print('Remove Role')
				await member.remove_roles(role)
		
		if channel:
			text = 'Removing Temprole **{0}**({0.id})'.format(member)
			embed=discord.Embed(
				title = 'Temprole Log',
				description = text,
				color=discord.Color(6253701)
			)
			await channel.send(embed=embed)

		task.cancel()

		# Remove task from list
		if task in self.temps:
			self.temps.remove(task)

	async def initialtemploop(self):
		if self.bot.debug: print('Starting temp loop test')
		for guild in self.bot.guilds:
			Users = self.settings.ServerConfig(guild.id, 'TempRoleUsers')
			if self.bot.debug: print(Users)
			if Users:
				for u in Users:
					_data = u.split('-')
					role = discord.utils.get(guild.roles, id=int(_data[1]))
					if self.bot.debug: print(_data[1])

					member = discord.utils.get(guild.members, id=int(_data[0]))
					if self.bot.debug: print(member)
					if self.bot.debug: print('Resuming Temprole Timer for: {0} in guild {1}({1.id}) for role: {2}'.format(member.name, guild, role))
					if self.bot.debug: print(role)
					self.temps.append(self.bot.loop.create_task(self.temploop(guild.id, member.id, role.id)))

	async def temploop(self, _guild, member, role):
		task = asyncio.current_task()
		for g in self.bot.guilds:
			if g.id == _guild: guild = g; break

		if self.bot.debug: 
			print(task)
			print('Temp loop')
			print(task.get_name())

		self.settings.TempConfig(guild.id, str(member), str(role), 'TempRoleTask', str(task.get_name()))

		_member = discord.utils.get(guild.members, id=int(member))
		_role = discord.utils.get(guild.roles, id=int(role))
		_LogChannel = discord.utils.get(guild.channels, id=int(self.settings.ServerConfig(guild.id, 'LogChannel')))
		_TemproleUser = discord.utils.get(guild.members, id=self.settings.TempConfig(guild.id, _member.id, _role.id, 'TempRoleUser', 0)) # User that added the inital temp role
		
		if self.bot.debug: 
			print(_role)
			print(_member)
			print(_LogChannel)
			print(_TemproleUser)

		if _LogChannel:
			_time_allocated = self.settings.TempConfig(guild.id, _member.id, _role.id, 'TempRoleTime', 0)
			if _TemproleUser:
				text = 'Adding Temprole **{0}**({0.id}) for {1} by: **{2}**({2.id})'.format(member, _time_allocated, _TemproleUser)
			else:
				text = 'Adding Temprole **{0}**({0.id}) for {1}'.format(member, _time_allocated)

			try:	
				embed=discord.Embed(
					title = 'Temprole Log',
					description = text,
					color=discord.Color(6208711)
				)
				await _LogChannel.send(embed=embed)
			except Exception as e:
				print(e)

		if _role: 
			while True:
				if self.bot.debug: print('Found Role')
				if not _role in _member.roles:
					if self.bot.debug: print('Add Role')
					await _member.add_roles(_role)
					if self.bot.debug: print('Role added')

				if self.bot.debug: print("Starting")
				_loop_start_time = int(time.time())

				if self.bot.debug: print(_loop_start_time)
				_init_time = self.settings.TempConfig(guild.id, _member.id, _role.id, 'TempRoleAdded')
				
				if self.bot.debug: print(_init_time)
				_time_allocated = self.settings.TempConfig(guild.id, _member.id, _role.id, 'TempRoleTime', 0)
				
				if self.bot.debug: print(_time_allocated)

				if self.bot.debug: print(_loop_start_time - _init_time)

				if _time_allocated <= (_loop_start_time - _init_time) or self.settings.TempConfig(guild.id, _member.id, _role.id, 'IsTemped') == False:
					if self.bot.debug: print('Users time is up')

					await self.TempEnd(guild, _role, _member, _LogChannel, task)
					self.settings.TempConfig(guild.id, _member.id, _role.id, 'IsTemped', False)
					self.settings.TempConfig(guild.id, _member.id, _role.id, passback='del')

					break
				else:
					# Get new time
					_time_to_wait = _time_allocated - (_loop_start_time - _init_time)
					if self.bot.debug: print('Time to wait {}'.format(_time_to_wait))

					# Update new time
					self.settings.TempConfig(guild.id, _member.id, _role.id, 'TempRoleTime', _time_to_wait)
					
					# Sleep function until it can remove
					await asyncio.sleep(_time_to_wait)

	###########################
	#  FUNCTION SECTION ENDS  #
	###########################

	@commands.command()
	async def temp(self, ctx, _user: commands.Greedy[discord.Member] = None, _role: discord.Role = None, *, _time = 10):
		"""[user][role][time(e.g. d1 h1 m1 s1 or 11121)]
		Adds a role to a user for a set amount of time. the role needs to be in the list of usable roles 
		"""

		_users = []

		_time_conv = self.settings.time_convert(_time) # Converts time

		if not _time_conv[1] >= 10: return await ctx.send('Time too short')

		if not _user or not _role: await ctx.send('Please input a valid user/users and role')

		if isinstance(_user, list):
			_users = _user
		else:
			print(_user)
			_users = [_user]

		_temp_roles = self.settings.ServerConfig(ctx.guild.id, 'TempRoles') # Acquires all roles that can be used to Temp

		# if not _role.id in _temp_roles:	return await ctx.send('Role not found in temp role list. Please do {}listtemprole'.format(self.settings.ServerConfig(ctx.guild.id, 'Prefix')))

		for user in _users:
			_is_tempted = self.settings.TempConfig(ctx.guild.id, user.id, _role.id, 'IsTemped')
			_temp_time = self.settings.TempConfig(ctx.guild.id, user.id, _role.id, 'TempRoleTime')
			
			if _is_tempted: 
				if self.bot.debug: print("adding time, user already tempted")
				end_time = _temp_time + _time_conv[1]
				self.settings.TempConfig(ctx.guild.id, user.id, _role.id, 'TempRoleTime', end_time)

				await ctx.send('Adding Temprole {} to {} for an extra {}'.format(_role, user, str(_time_conv[0])))

			if not _is_tempted:
				if self.bot.debug: print("Adding temp role to user")
				_start_time = int(time.time())

				if self.bot.debug: print('Start time is {}'.format(_start_time))
				self.settings.TempConfig(ctx.guild.id, user.id, _role.id, "IsTemped", True)
				self.settings.TempConfig(ctx.guild.id, user.id, _role.id, "TempRoleAdded", _start_time)
				self.settings.TempConfig(ctx.guild.id, user.id, _role.id, "TempRoleUser", ctx.author.id)
				
				if self.bot.debug: print(_time_conv[1])
				self.settings.TempConfig(ctx.guild.id, user.id, _role.id, 'TempRoleTime',  _time_conv[1])

				if self.bot.debug: print('Adding user to temp loop')
				self.temps.append(self.bot.loop.create_task(self.temploop(ctx.guild.id, user.id, _role.id)))
				
				await ctx.send('Adding Temprole {} to {} for {}'.format(_role, user, _time_conv[0]))

	@commands.command()
	async def stoptemp(self, ctx, _user: commands.Greedy[discord.Member] = None, _role: discord.Role = None):
		"""[user][role]
		Unmutes User. 
		"""

		if not isinstance(_user, list):
			_user = [_user]
		
		guild = ctx.guild
		channel = discord.utils.get(guild.channels, id=self.settings.ServerConfig(guild.id, 'LogChannel'))	
		_temp_roles = self.settings.ServerConfig(ctx.guild.id, 'TempRoles') # Acquires all roles that can be used to Temp

		for _member in _user:
			if _role in _member.roles and _role.id in _temp_roles: 
				# Found role remove it from user
				msg = await ctx.send('Removing <@&{}> from {} by **{}**'.format(_role.id, _member.name, ctx.author.name))
			
				# get task:
				task = None
				_task_number = self.settings.MuteConfig(guild.id, _member.id, 'MuteTask')
				for t in self.mutes:
					if t.get_name() == _task_number: task = t

				await self.TempEnd(self, guild, _role, _member, channel, task)
			
				# IsTempted to False
				self.settings.TempConfig(guild.id, _member.id, _role.id, 'IsTemped', False)

				# Remove from list
				self.settings.TempConfig(guild.id, _member.id, _role.id, passback='del')
				
				await msg.edit(content='Removed Temprole <@{}> from User {}'.format(_role.id, _member.name))
			else:
				await msg.edit(content='Unable to find Temprole <@{}> in {} roles'.format(_role.id, _member.name))

	@commands.command()
	async def listtemprole(self, ctx):
		"""Lists all the temp roles availible
		"""

		_roles_list = []
		
		_roles = self.settings.ServerConfig(ctx.guild.id, 'TempRoles')
		for x in _roles:
			r = discord.utils.get(ctx.guild.roles, id=int(x))
			if r: _roles_list.append('<@&{}>'.format(r.id))
		
		if ctx.author.top_role.colour:
			col = ctx.author.top_role.colour
		else:
			col =self.settings.randomColor()

		embed = discord.Embed(
			title = 'Temp roles',
			description = '\n'.join(_roles_list),
			colour = col
		)
		await ctx.send(embed=embed)

	@commands.command()
	async def addtemprole(self, ctx, *, _roles: discord.Role = None ):
		"""[role]
		Adds role to temp role list
		"""

		if not isinstance(_roles, list):
			_roles = [_roles]

		# Checks if role exists
		for role in _roles:
			if not role:
				await ctx.send('Unable to find role: '.format(role))
				await ctx.send('Do you want to create it? y/n')
				channel = ctx.channel
				author = ctx.author

				def check(m):
					return m.channel == channel and m.author == author

				msg = await self.bot.wait_for('message', check=check)
				if str(msg.content).lower() == 'n':
					return await ctx.send('Please type in another role name')

				elif str(msg.content).lower() == 'y':
					col = self.settings.randomColor()
					role = await ctx.guild.create_role(name=role, color=col)
				else:
					return

			# Adds role
			_users = self.settings.ServerConfig(ctx.guild.id, 'TempRoles')
			if not role.id in _users:
				_users.append(role.id)
				print(_users)
		
			self.settings.ServerConfig(ctx.guild.id, 'TempRoles', _users)

			await ctx.send('I have added {} to Temp role list. There are now {} roles'.format(role, len(_users)))

	@commands.command()
	async def remtemprole(self, ctx, _roles: commands.Greedy[discord.Role] = None ):
		"""[role]
		Removes role from temp role list
		"""
		# Checks if role exists
		if not isinstance(_roles, list):
			_roles = [_roles]

		# Checks if role exists
		for role in _roles:
			# Remove role
			_users = self.settings.ServerConfig(ctx.guild.id, 'TempRoles')
			if role.id in _users:
				_users.remove(role.id)

			self.settings.ServerConfig(ctx.guild.id, 'TempRoles', _users)

			await ctx.send('I have removed {} from Temp role list. There are now {} roles'.format(role, len(_users)))
