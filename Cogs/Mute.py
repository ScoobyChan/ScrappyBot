# Check in onjoin that if muted keep
import asyncio
import discord
from discord.ext import commands
from discord.ext.commands import MemberConverter

def setup(bot):
	settings = bot.get_cog("Settings")
	bot.add_cog(Mute(bot, settings))

class Mute(commands.Cog):
	def __init__(self, bot, settings):
		self.bot = bot
		self.settings = settings
		self.converter = MemberConverter()
		self.mutes = []

	@commands.Cog.listener()
	async def on_unloaded_extension(self, ext):
		# Cancel mutes
		for task in self.mutes:
			task.cancel()

	@commands.Cog.listener()
	async def on_loaded_extension(self, ext):
		# Waits till Bot is ready
		await self.bot.wait_until_ready()
		# print("Initializing the Mutes")

		await self.initialmuteloop()

	async def MuteEnd(self, guild, role, member, channel, task):
		if role:
			# print('Found Role')
			if role in member.roles:
				# print('Remove Role')
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

	async def initialmuteloop(self):
		for guild in self.bot.guilds:
			Users = self.settings.ServerConfig(guild.id, 'MutedUsers')
			for member in Users:
				print('Resuming Mute Time for: {} in guild ID ({})'.format(self.bot.get_user(int(member)), guild))
				self.mutes.append(self.bot.loop.create_task(self.muteloop(guild.id, member)))

	async def muteloop(self, Guild, member):
		task = asyncio.Task.current_task()
		self.settings.setTempConfig(guild.id, str(member.id), 'MuteTask', task)

		# print('Mute Loop')
		for g in self.bot.guilds:
			if int(g.id)  == int(Guild):
				guild = g
				break

		# Settings
		_users = self.settings.ServerConfig(guild.id, 'MutedUsers')
		LogChannel = self.settings.ServerConfig(guild.id, 'LogChannel')

		# Fetch users and mute role
		role = discord.utils.get(guild.roles, id=self.settings.ServerConfig(guild.id, 'MuteRole'))
		member = discord.utils.get(self.bot.get_all_members(), id=int(member))
		channel = discord.utils.get(self.bot.get_all_channels(), id=LogChannel)
		MuteUser = discord.utils.get(self.bot.get_all_members(), id=_users.get(str(member.id), {}).get('MuteUser', 0))

		# get users mute time
		Time = _users.get(str(member.id), {}).get('MuteTime', 0)

		# print(Time)

		if channel:
			if MuteUser:
				text = 'Muting **{0}**({0.id}) for {1}\nMuted by: **{2}**({2.id})'.format(member, Time, MuteUser)
			else:
				text = 'Muting **{0}**({0.id}) for {1}'.format(member, Time)

			try:	
				embed=discord.Embed(
					title = 'Mute Log',
					description = text,
					color=discord.Color(6208711)
				)
				await channel.send(embed=embed)
			except Exception as e:
				print(e)

		# If muted Add role to user
		if role:
			# print('Found Role')
			if not role in member.roles:
				# print('Add Role')
				await member.add_roles(role)
		else:
			overwrite = discord.PermissionOverwrite()
			overwrite.send_messages = False
			overwrite.speak = False
			overwrite.read_messages = True
			for c in guild.channels:
				if type(c) != discord.CategoryChannel:
					await c.set_permissions(member, overwrite=overwrite)

		while True:
			Start = int(time.time())
			Init = self.settings.getMuteConfig(guild.id, str(member.id), 'MuteAdded')
			Unlimitedmute = self.settings.getMuteConfig(guild.id, str(member.id), 'Unlimited')
			if not Unlimitedmute or Unlimitedmute == False:	
				if self.settings.getMuteConfig(guild.id, str(member.id), 'MuteTime') <= (Start - Init) or self.settings.getMuteConfig(guild.id, str(member.id), 'IsMuted') == False:
					Users = self.settings.ServerConfig(guild.id, 'MutedUsers')
					
					# Unmute user
					await self.MuteEnd(guild, role, member, channel, task)

					# Remove Muted user
					del Users[str(member.id)]
					self.settings.ServerConfig(guild.id, 'MutedUsers', Users)
					break

				else:
					_time = self.settings.getMuteConfig(guild.id, str(member.id), 'MuteTime') - (Start - Init)
					self.settings.setMuteConfig(guild.id, str(member.id), 'MuteTime', _time)
					self.settings.setMuteConfig(guild.id, str(member.id), 'MuteAdded', Start)

					# Sleep for x
				await asyncio.sleep(_time)
			else:
				await asyncio.sleep(1)

	async def _mute(self, ctx, member, channel, guild):
		if not member:
			return await ctx.send('Can\'t find user {}'.format(_member))

		# Check if User
		_users = self.settings.ServerConfig(guild.id, 'MutedUsers')
		if str(member.id) in _users:
			# increase time if needed
			self.settings.setMuteConfig(guild.id, str(member.id), 'MuteTime', (self.settings.getMuteConfig(guild.id, str(member.id), 'MuteTime') + mute_time))
			await ctx.send('Muting {} for extra {} by **{}**'.format(member.name, mute_time, ctx.author.name))
		else:
			# Add User
			self.settings.newMuteConfig(guild.id, member.id)
			# Add Time

			if mute_time == -1:	
				# Unlimited Timer
				self.settings.setMuteConfig(guild.id, member.id, setting, arg1, arg2=None)
			else:
				# Normal Timer
				_time = self.settings.Time(mute_time)
				self.settings.setMuteConfig(guild, user, 'MuteTime')

			await ctx.send('Muting {} for {} by **{}**'.format(member.name, mute_time, ctx.author.name))
			self.mutes.append(self.bot.loop.create_task(self.muteloop(guild.id, member.id)))

	@commands.command()
	async def mute(self, ctx, _member=None, *, mute_time=None):
		"""
		[Member][time(e.g. d1 h1 m1 s1 or 11121)]
		Mutes a member for a certain amount of time
		"""

		member = self.settings.Get(ctx, 'user', _member)
		channel = discord.utils.get(self.bot.get_all_channels(), id=self.settings.ServerConfig(guild.id, 'LogChannel'))
		guild = ctx.guild

		await self._mute(ctx, member, channel, guild)
		
		
	@commands.command()
	async def unmute(self, ctx, _member=None):
		"""[user]
		Unmutes User. 
		"""

		member = self.settings.Get(ctx, 'user', _member)
		role = discord.utils.get(guild.roles, id=self.settings.ServerConfig(guild.id, 'MuteRole'))
		channel = discord.utils.get(self.bot.get_all_channels(), id=self.settings.ServerConfig(guild.id, 'LogChannel'))
		guild = ctx.guild

		if not member:
			await ctx.send('Can\'t find user {}'.format(_member))

		msg = await ctx.send('Unmuting {} by **{}**'.format(member.name, ctx.author.name))
		# Remove Role/Perms
		await msg.edit(content='Removing Perms/Role')
		await self.MuteEnd(guild, role, member, channel)

		# Unlimited to False
		self.settings.setMuteConfig(guild.id, str(member.id), 'Unlimited', False)
		# IsMuted to False
		self.settings.setMuteConfig(guild.id, str(member.id), 'IsMuted', False)
		# Cancel
		# self.settings.getMuteConfig(guild.id, str(member.id), 'MuteTask').cancel()

		await msg.edit(content='Unmuted User {}'.format(member.name))
	
	@commands.command()
	async def muterole(self, ctx):
		"""Displays the mute role"""
		msg = await ctx.send('Collecting Mute Role')
		await asyncio.sleep(1)
		role = self.settings.Get(ctx, 'role', self.settings.ServerConfig(ctx.author.id, 'MuteRole'))
		await msg.edit(content=('Mute Role is set to: **{0}** ({0.id}) '.format(role) if role else 'No Mute Role found'))

	@commands.command()
	async def setmuterole(self, ctx, MuteRoleName='Muted'):
		"""[rolename]
		Sets the mute role with the right permissions too (May need to move it into the right position"""
		color = self.settings.randomColor()

		overwrite = discord.PermissionOverwrite()
		overwrite.send_messages = False
		overwrite.speak = False
		overwrite.read_messages = True

		msg = await ctx.send('Finding Role: **%s**' % MuteRoleName)
		role = self.settings.Get(ctx, 'role', MuteRoleName)
		l = self.settings.LoadSettings()

		if MuteRole:
			if not role:
				# Creates the role if missing
				await msg.edit(content='Creating Role: **%s**' % MuteRoleName)
				role = await guild.create_role(name=MuteRoleName, colour=color)

			await asyncio.sleep(1)
			await msg.edit(content='Syncing Role: **%s**' % role)

			for c in ctx.guild.channels:
				if type(c) != discord.CategoryChannel:
					await c.set_permissions(role, overwrite=overwrite)

			await asyncio.sleep(1)
			await msg.edit(content='Role: **%s** has synced with the channels' % role)

			self.settings.ServerConfig(ctx.author.id, 'MuteRole', role.id)
		else:
			self.settings.ServerConfig(ctx.author.id, 'MuteRole', 0)
		
		embed = discord.Embed(
			title="I have set Mute role: %s" % MuteRoleName,
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
		role = self.settings.Get(ctx, 'role', self.settings.ServerConfig(guild.id, 'MuteRole'))
		
		if role:
			for c in ctx.guild.channels:
				if type(c) != discord.CategoryChannel:
					await c.set_permissions(role, overwrite=overwrite)

	@commands.command()
	async def desyncmuterole(self, ctx):
		"""Desyncs Roles and Users from Channels"""
		
		guild = ctx.guild
		role = self.settings.Get(ctx, 'role', self.settings.ServerConfig(guild.id, 'MuteRole'))
		
		if role:
			for c in ctx.guild.channels:
				if type(c) != discord.CategoryChannel:
					await c.set_permissions(role, overwrite=None)