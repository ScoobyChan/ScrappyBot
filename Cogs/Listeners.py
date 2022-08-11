# Log guilds
from Utils import Configuration

import os
import discord
from discord.ext import commands
from discord.ext.commands import MemberConverter

def setup(bot):
	settings = bot.get_cog("Settings")
	bot.add_cog(Listeners(bot, settings))

class Listeners(commands.Cog):
	def __init__(self, bot, settings):
		self.bot = bot
		self.settings = settings
		self.Conf = Configuration.Configuration(bot)

	
	async def onguildjoin(self, guild):
		# Check if in blacklist
		BlackL = self.settings.getBotConfig('BlacklistedServers', [])
		if guild.id in BlackL:
			await guild.leave()
			raise commands.NoEntryPointError('{} is blacklisted and I am not allowed to join this server'.format(guild))
			return 

		# add new Server
		self.Conf.UpdateJson(guild.id)
		
		if self.settings.ServerConfig(guild.id, 'DefaultRole') == 0:
			print('Default Role: %s' % discord.utils.get(guild.roles, name='@everyone'))
			Role = discord.utils.get(guild.roles, name='@everyone').id
			self.settings.ServerConfig(guild.id, 'DefaultRole', Role)
	
	async def onguildremove(self, guild):
		# Remove Server Config
		for Json in os.listdir('Json/Servers'):
			if Json.startswith(str(guild.id)):
				os.remove('Json/Servers/'+Json)

		# Remove User Config
		for Json in os.listdir('Json/Users'):
			if Json.startswith(str(guild.id)):
				os.remove('Json/Users/'+Json)

	async def onmemberjoin(self, member):
		guild = member.guild
		
		if self.settings.ServerConfig(member.guild.id, 'DefaultRole') != 0:
			r = self.settings.Get(member, 'role', self.settings.ServerConfig(member.guild.id, 'DefaultRole'))
			await member.add_roles(r)
			
		# To happen
		# - Create user config
		self.settings.UserConfig(guild.id, member.id, 'XP')

		# - Message Log Channel
		log = self.settings.ServerConfig(guild.id, 'LogChannel')
		if log != 0:
			await log.send('{} has joined the server {}'.format(member, guild))	# Make this an embed

		# - Message Welcome Channel
		ch = self.settings.ServerConfig(guild.id, 'WelcomeChannel')
		msg = self.settings.ServerConfig(guild.id, 'WelcomeMsg')

		Users = []
		for user in guild.members:
			if str(user.status) != 'offline':
				Users.append(user.name)

		if ch != 0 and msg != None:
			ch = discord.utils.get(self.bot.get_all_channels(), id=int(ch))
			await ch.send(msg)	# Make this an embed

			msg = msg.replace('[[user]]', member.name).replace('[[userID]]', str(member.id)).replace('[[atuser]]', member.mention).replace('[[server]]', member.guild.name).replace('[[UserCount]]', str(len(member.guild.members))).replace('[[online]]', str(len(Users)))

		# Add onjoin role
		r = self.settings.Get(member, 'role', self.settings.ServerConfig(guild.id, 'DefaultRole'))
		m = self.settings.Get(member, 'user', member.id)
		converter = MemberConverter()
		# member = await converter.convert(ctx, str(member))
		# print(r)
		# print(m)
		mem = await converter.convert(member, str(m))
		if r:
			await mem.add_roles(r)
			
			if self.settings.ServerConfig(guild.id, 'isLockedDown'):
				lockr = self.settings.Get(member, 'role', self.settings.ServerConfig(guild.id, 'Lockdown'))
				await mem.add_roles(lockr)

		######### Optional ###########
		# - Voice Stats
		vc = self.settings.Get(member, 'channel', self.settings.ServerConfig(guild.id, 'VcStatChannel'))
		if vc:
			msg = 'VC Member Count: ' + str(len(guild.members))
			await vc.edit(name=msg)
		
		# - Online Users ---- Unsure how to loop this
		# onm = self.settings.Get(member, 'channel', self.settings.ServerConfig(guild.id, 'OnlStatChannel'))
		# if onm:
		# 	msg = 'Online Member Count: ' + str(len(guild.members) - len(Users))
		# 	await onm.edit(name=msg)

		# - User Count
		memChan = self.settings.Get(member, 'channel', self.settings.ServerConfig(guild.id, 'MemStatChannel'))
		if memChan:
			msg = 'Member Count: ' + str(len(guild.members))
			await memChan.edit(name=msg)

		# Check if Muted
		if mem.id in self.settings.ServerConfig(guild.id, 'MutedUsers'):
			role = discord.utils.get(guild.roles, id=self.settings.ServerConfig(guild.id, 'MuteRole'))
			logchannel = discord.utils.get(self.bot.get_all_channels(), id=self.settings.ServerConfig(guild.id, 'LogChannel'))
			
			_Mute = self.bot.get_cog('Mute')
			_Mute.mutes.append(self.bot.loop.create_task(_Mute.muteloop(guild.id, mem.id)))

		if self.settings.ServerConfig(member.guild.id, 'DefaultRole') != 0:
			r = self.settings.Get(member, 'role', self.settings.ServerConfig(member.guild.id, 'DefaultRole'))
			await member.add_roles(r)
	
	async def onmemberremove(self, member): 
		guild = member.guild
		# To happen
		# - Create user config
		self.settings.UserConfig(guild.id, member.id, 'XP')

		# - Message Log Channel
		log = self.settings.ServerConfig(guild.id, 'LogChannel')
		if log != 0:
			await log.send('{} has joined the server {}'.format(member, guild))	# Make this an embed

		# - Message Welcome Channel
		ch = self.settings.ServerConfig(guild.id, 'GoodByeChannel')
		msg = self.settings.ServerConfig(guild.id, 'GoodByeMsg')

		Users = []
		for user in guild.members:
			if str(user.status) != 'offline':
				Users.append(user.name)

		if ch != 0 and msg != None:
			ch = discord.utils.get(self.bot.get_all_channels(), id=int(ch))
			msg = msg.replace('[[user]]', member.name).replace('[[userID]]', str(member.id)).replace('[[atuser]]', member.mention).replace('[[server]]', member.guild.name).replace('[[UserCount]]', str(len(member.guild.members))).replace('[[online]]', str(len(Users)))
			await ch.send(msg)	# Make this an embed




		######### Optional ###########
		# - Voice Stats
		vc = self.settings.Get(member, 'channel', self.settings.ServerConfig(guild.id, 'VcStatChannel'))
		if vc:
			msg = 'VC Member Count: ' + str(len(guild.members))
			await vc.edit(name=msg)
		
		# - Online Users ---- Unsure how to loop this
		# onm = self.settings.Get(member, 'channel', self.settings.ServerConfig(guild.id, 'OnlStatChannel', 0))
		# if onm:
		# 	msg = 'Online Member Count: ' + str(len(guild.members) - len(Users))
		# 	await onm.edit(name=msg)

		# - User Count
		mem = self.settings.Get(member, 'channel', self.settings.ServerConfig(guild.id, 'MemStatChannel'))
		if mem:
			msg = 'Member Count: ' + str(len(guild.members))
			await mem.edit(name=msg)
