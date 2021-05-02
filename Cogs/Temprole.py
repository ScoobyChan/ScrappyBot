import asyncio
import discord
from discord.ext import commands

def setup(bot):
	settings = bot.get_cog("Settings")
	bot.add_cog(Temprole(bot, settings))

class Temprole(commands.Cog):
	def __init__(self, bot, settings):
		self.bot = bot
		self.settings = settings
		self.temps = []

	@commands.Cog.listener()
	async def on_unloaded_extension(self, ext):
		# Cancel mutes
		for task in self.temps:
			task.cancel()

	@commands.Cog.listener()
	async def on_loaded_extension(self, ext):
		# Waits till Bot is ready
		await self.bot.wait_until_ready()
		# print("Initializing the Temp roles")

		await self.initialmuteloop()

	async def TempEnd(self, guild, role, member, channel, task):
		if role:
			# print('Found Role')
			if role in member.roles:
				# print('Remove Role')
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

	async def initialmuteloop(self):
		for guild in self.bot.guilds:
			Users = self.settings.ServerConfig(guild.id, 'TempRoleUsers')
			for u in Users:
				_data = u.split('-')
				role = discord.utils.get(guild.roles, id=int(_data[1]))
				member = discord.utils.get(self.bot.get_all_members(), id=int(_data[1]))
				print('Resuming Temprole Timer for: {0} in guild {1}({1.id}) for role: {2}'.format(member.name, guild, role))
				self.temps.append(self.bot.loop.create_task(self.temploop(guild.id, member.id, role.id)))

	async def temploop(self, Guild, member, Role):
		task = asyncio.Task.current_task()
		self.settings.TempConfig(guild.id, str(member.id), 'TempRoleTask', task)

		# print('Mute Loop')
		for g in self.bot.guilds:
			if int(g.id)  == int(Guild):
				guild = g
				break

		# Settings
		_users = self.settings.ServerConfig(guild.id, 'TempRoleUsers')
		LogChannel = self.settings.ServerConfig(guild.id, 'LogChannel')

		# Fetch users and mute role
		role = discord.utils.get(guild.roles, id=Role)
		member = discord.utils.get(self.bot.get_all_members(), id=int(member))
		channel = discord.utils.get(self.bot.get_all_channels(), id=LogChannel)
		MuteUser = discord.utils.get(self.bot.get_all_members(), id=_users.get(str(member.id)+'-'+str(role.id), {}).get('TempRoleUser', 0))

		# get users mute time
		Time = _users.get(str(member.id)+'-'+str(role.id), {}).get('TempRoleTime', 0)

		# print(Time)

		if channel:
			if MuteUser:
				text = 'Adding Role **{0}**({0.id}) for {1}\ by: **{2}**({2.id})'.format(member, Time, MuteUser)
			else:
				text = 'Muting **{0}**({0.id}) for {1}'.format(member, Time)

			try:	
				embed=discord.Embed(
					title = 'Temprole Log',
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

			while True:
				Start = int(time.time())
				Init = self.settings.TempConfig(guild.id, str(member.id)+'-'+str(role.id), 'TempRoleAdded')

				if self.settings.TempConfig(guild.id, str(member.id)+'-'+str(role.id), 'TempRoleTime') <= (Start - Init) or self.settings.TempConfig(guild.id, str(member.id)+'-'+str(role.id), 'IsTemped') == False:
					Users = self.settings.ServerConfig(guild.id, 'TempRoleUsers')
					
					# Untemprole user
					await self.TempEnd(guild, role, member, channel, task)

					# Remove Muted user
					del Users[str(member.id)+'-'+str(role.id)]

					self.settings.ServerConfig(guild.id, 'TempRoleUsers', Users)
					break

				else:
					_time = self.settings.TempConfig(guild.id, str(member.id)+'-'+str(role.id), 'TempRoleTime') - (Start - Init)
					self.settings.TempConfig(guild.id, str(member.id), 'MuteTime', _time)
					self.settings.TempConfig(guild.id, str(member.id), 'MuteAdded', Start)

					# Sleep for x
					await asyncio.sleep(_time)

	@commands.command()
	async def temprole(self, ctx, user: discord.Member = None, role: discord.Role = None, time: int = 10):
		"""[user][role][time]
		Adds a role to a user for a set amount of time. the role needs to be in the list of usable roles 
		"""

		if not time > 10:
			return await ctx.send('Time too short')
		# inits
		guild = ctx.guild
		_Roles = self.settings.ServerConfig(guild.id, 'TempRoles')
		role = self.settings.Get(ctx, 'role', role)
		if not role:
			return

		if not role.id in _Roles:
			return

		member = self.settings.Get(ctx, 'user', user)

		_time = self.settings.Time()
		await ctx.send('Adding Temprole: {} to {} for {}'.format(role, member, _time[1]))

		self.settings.newTempConfig(guild.id, str(member.id)+'-'+str(role.id))

		# Adds to Json
		self.settings.TempConfig(guild.id, str(member.id)+'-'+str(role.id), 'TempRoleTime', _time[0])
		self.settings.TempConfig(guild.id, str(member.id)+'-'+str(role.id), 'TempRoleUser', ctx.author.id)
		self.temps.append(self.bot.loop.create_task(self.temploop(guild.id, member.id, role.id)))
		
	@commands.command()
	async def stoptemprole(self, ctx, user):
		"""[user]
		Untemproles User. 
		"""
		guild = ctx.guild
		_users = self.settings.ServerConfig(guild.id, 'TempRoleUsers')
		member = self.settings.Get(ctx, 'user', _member)
		role = discord.utils.get(guild.roles, id=self.settings.ServerConfig(guild.id, 'MuteRole'))
		channel = discord.utils.get(self.bot.get_all_channels(), id=self.settings.ServerConfig(guild.id, 'LogChannel'))

		if not member:
			await ctx.send('Can\'t find user {}'.format(_member))

		msg = await ctx.send('Unmuting {} by **{}**'.format(member.name, ctx.author.name))
		# Remove Role/Perms
		await msg.edit(content='Removing Perms/Role')
		await self.MuteEnd(guild, role, member, channel)

		# IsMuted to False
		self.settings.setMuteConfig(guild.id, str(member.id), 'IsTemped', False)

		await msg.edit(content='Unmuted User {}'.format(member.name))

	@commands.command()
	async def addtemprole(self, ctx, role):
		"""[role]
		Adds role to temp role list
		"""
		# Checks if role exists
		role = self.settings.Get(ctx, 'role', role)
		if not role:
			col = self.settings.randomColor()
			role = await ctx.guild.create_role(name=roleName, color=col)

		# Adds role
		_users = self.settings.ServerConfig(guild.id, 'TempRoles')
		if role.id in _users:
			_users.append(role.id)
		
		self.settings.ServerConfig(guild.id, 'TempRoles'. _users)

		await ctx.send('I have added {} to Temp role list. There are now {} roles'.format(role, len(_users)))

	@commands.command()
	async def remtemprole(self, ctx, role):
		"""[role]
		Removes role from temp role list
		"""
		# Checks if role exists
		role = self.settings.Get(ctx, 'role', role)
		if not role:
			return

		# Remove role
		_users = self.settings.ServerConfig(guild.id, 'TempRoles')
		if role.id in _users:
			_users.remove(role.id)

		self.settings.ServerConfig(guild.id, 'TempRoles'. _users)

		await ctx.send('I have removed {} from Temp role list. There are now {} roles'.format(role, len(_users)))

	@commands.command()
	async def listtemprole(self, ctx):
		"""Lists all the temp roles availible
		"""
		_users = self.settings.ServerConfig(guild.id, 'TempRoles')
		msg = ''
		for role in _roles:
			msg += '\n{}'.format(self.settings.Get(ctx, 'role', role).mention)

		if ctx.author.top_role.colour:
			col = ctx.author.top_role.colour
		else:
			col =self.settings.randomColor()

		embed = discord.Embed(
			title = 'Temp roles',
			description = msg,
			colour = col
		)
		await ctx.send(embed=embed)