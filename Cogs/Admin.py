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


		if self.bot.get_cog('Perms'):
			self.bot.kic_ban.append('ban')
			self.bot.kic_ban.append('kick')
			self.bot.kic_ban.append('unban')

	@commands.Cog.listener()
	async def on_unloaded_extension(self, ext):
		# Cancel tempbans
		for task in self.tempbans:
			task.cancel()

	@commands.Cog.listener()
	async def on_loaded_extension(self, ext):
		# Waits till Bot is ready
		await self.bot.wait_until_ready()
		# print("Initializing the Mutes")
		await self.initialtempban()

	async def TempBanEnd(self, guild, member, task):
		bans = [b.user.id for b in await guild.bans()]
		if member.id in bans:
			await guild.unban(member)
		
		task.cancel()

	async def initialtempban(self):
		for guild in self.bot.guilds:
			Users = self.settings.ServerConfig(guild.id, 'TempBan')
			for member in Users:
				print('Resuming Temp Ban Time for: {} in guild ID ({})'.format(self.bot.get_user(int(member)), guild))
				self.tempbans.append(self.bot.loop.create_task(self.banloop(guild, member)))

	async def banloop(self, Guild, member):
		task = asyncio.Task.current_task()
		self.settings.BanConfig(guild.id, str(member.id), 'Task', task)

		# print('Mute Loop')
		for g in self.bot.guilds:
			if int(g.id)  == int(Guild.id):
				guild = g
				break

		# Settings
		_users = self.settings.ServerConfig(guild.id, 'TempBan')
		LogChannel = self.settings.ServerConfig(guild.id, 'LogChannel')

		# Fetch users and mute role
		member = discord.utils.get(self.bot.get_all_members(), id=int(member))
		channel = discord.utils.get(self.bot.get_all_channels(), id=LogChannel)

		# get users mute time
		Time = _users.get(str(member.id), {}).get('bantime', 0)
		
		while True:
			Start = int(time.time())
			Init = self.settings.BanConfig(guild.id, str(member.id), 'bantime')
			if self.settings.BanConfig(guild.id, str(member.id), 'bantime') <= (Start - Init) or self.settings.BanConfig(guild.id, str(member.id), 'banned') == False:
				Users = self.settings.ServerConfig(guild.id, 'TempBan')
				
				# Unmute user
				await self.TempBanEnd(guild, member, task)

				# Remove Muted user
				del Users[str(member.id)]
				self.settings.ServerConfig(guild.id, 'TempBan', Users)
				break

			else:
				_time = self.settings.BanConfig(guild.id, str(member.id), 'bantime') - (Start - Init)
				self.settings.BanConfig(guild.id, str(member.id), 'bantime', _time)

				# Sleep for x
			await asyncio.sleep(_time)


	@commands.command()
	async def listban(self, ctx):
		"""
		Lists the users banned
		"""

		for b in await ctx.guild.bans():
			text = f"{b.user.name}#{b.user.discriminator}\n -> ```\n{b.reason}\n```"
			embed = discord.Embed(
				description = text,
				colour = 0x32a8a6
			)
			await ctx.send(embed=embed)

	@commands.command()
	async def kick(self, ctx, user=None, *, reason=None):
		"""
		[user] [reason]
		This is used to kick users
		"""
		u = self.settings.Get(ctx, 'user', user)
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
		time.sleep(0.05)

		def check(m):
			return m.content == str(con) and m.channel == channel and m.author == user

		try:
			t = await self.bot.wait_for('message', timeout=10, check=check)
		except asyncio.exceptions.TimeoutError:
			await msg.delete()
			await ctx.send('Kick Attempt of **' + str(u.name) + '** cancelled')
			return

		await msg.delete()
		await t.delete()
		await ctx.send('`I have kicked: ' + u.name + '`')
		await ctx.guild.kick(u, reason=reason)


	@commands.command()
	async def ban(self, ctx, user=None, reason=None, ban_time=None):
		"""
		[user] [reason] [time/optional]
		This is used to ban users with the ban hammer
		"""
			
		u = self.settings.Get(ctx, 'user', user)
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
		time.sleep(0.05)

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
		await ctx.send(f'`I have banned: {u.name}`') # Add time
		await ctx.guild.ban(u, reason=reason, delete_message_days=10)

		if time:
			_users = self.settings.ServerConfig(guild.id, 'TempBan')
			if str(member.id) in _users:
				self.settings.BanConfig(guild.id, str(member.id), 'bantime', (self.settings.BanConfig(guild.id, str(member.id), 'bantime') + ban_time))
			else:
				self.settings.newBanConfig(guild.id, member.id)
				_time = self.settings.Time(mute_time)
				self.settings.BanConfig(guild, user, 'bantime', _time)
				self.tempbans.append(self.bot.loop.create_task(self.banloop(ctx.guild.id, u)))


	@commands.command()
	async def unban(self, ctx, userID=None, reason=None):
		"""
		[user ID] [reason]
		used to unban members
		"""

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
		time.sleep(0.05)

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

		await ctx.send('`I have unbanned: ' + u.name + '`')
		await ctx.guild.unban(u, reason=reason)

		self.settings.BanConfig(guild.id, str(member.id), 'banned', False)