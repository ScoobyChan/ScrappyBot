from Utils import Utils
import discord
from discord.ext import commands

def setup(bot):
	settings = bot.get_cog("Settings")
	bot.add_cog(Logging(bot, settings))

class Logging(commands.Cog):
	def __init__(self, bot, settings):
		self.bot = bot
		self.settings = settings
		self.Utils = Utils.Utils()

		self.listeners = ['bulk.msg.delete', 'guild.chan.delete', 'guild.chan.create', 'guild.chan.update', 
						'guild.role.create', 'guild.role.delete', 'guild.role.update',
						'member.join', 'member.remove', 'member.ban', 'member.unban',
						'message.edit', 'message.delete',
						'invite.create', 'invite.send', 'invite.delete',
						'member.edit.nick', 'member.edit.name', 'member.edit.avatar', 'member.edit.activity']
		self.basic = ['member.join', 'invite.create']
		self.member = ['message.edit', 'message.delete', 'member.join', 'member.remove', 'member.ban', 'member.unban', 'member.edit.nick', 'member.edit.name', 'member.edit.avatar', 'member.edit.activity']
		self.advanced_member = ['guild.role.create', 'guild.role.delete', 'guild.role.update', 'member.join', 'member.remove', 'member.ban', 'member.unban', 'member.edit.nick', 'member.edit.name', 'member.edit.avatar', 'member.edit.activity']
		self.message = ['bulk.msg.delete', 'guild.chan.delete', 'guild.chan.create', 'guild.chan.update', 'message.edit', 'message.delete']
		self.invite = ['invite.create', 'invite.send', 'invite.delete']
		self.guild_related = ['guild.chan.delete', 'guild.chan.create', 'guild.chan.update', 'guild.role.create', 'guild.role.delete', 'guild.role.update']

		self.presets = ["all", "basic", "member", "advanced_member", "message", "invite", "guild_related"]

		self.invite_list = {}

	# https://discordpy.readthedocs.io/en/latest/api.html#event-reference
	# Enable options of different options to log

	@commands.Cog.listener()
	async def on_loaded_extension(self, ext):
		# Adds Invite lists to
		await self.bot.wait_until_ready()
		for guild in self.bot.guilds:
			try:
				self.invite_list[str(guild.id)] = await guild.invites()
			except:
				pass

	@commands.command()
	async def enablelogging(self, ctx):
		"""Enabled logging to set channel for the server"""
		if self.settings.ServerConfig(ctx.guild.id, 'Logging') == True:
			await ctx.send('Server Logging Disabled')
			self.settings.ServerConfig(ctx.guild.id, 'Logging', False)
		else:
			if self.settings.ServerConfig(ctx.guild.id, 'LogChannel') == 0:
				return await ctx.send('Please set Logging Channel')
			await ctx.send('Server Logging Enabled')
			self.settings.ServerConfig(ctx.guild.id, 'Logging', True)

	@commands.command()
	async def setloggingchannel(self, ctx, ch=None):
		"""[channel]
		Sets logging channel for server"""
		if ch == 0:
			self.settings.ServerConfig(ctx.guild.id, 'LogChannel', 0)
			self.settings.ServerConfig(ctx.guild.id, 'Logging', False)

			await ctx.send('I have disabled Logging')
			return

		if not ch:	
			ch = ctx.channel.id
		c = self.settings.Get(ctx, 'channel', ch)
		
		self.settings.ServerConfig(ctx.guild.id, 'LogChannel',c.id)
		self.settings.ServerConfig(ctx.guild.id, 'Logging', True)
		self.settings.ServerConfig(ctx.guild.id, 'LoggingType', self.basic)
		await ctx.send('Setting Logging channel to: **' + str(c) + '** with the basic logging settings')

	@commands.command()
	async def testlogging(self, ctx):
		"""Sends a test message to logging channel"""
		c = self.settings.Get(ctx, 'channel', self.settings.ServerConfig(ctx.guild.id, 'LogChannel'))
		if c:
			if self.settings.ServerConfig(ctx.guild.id, 'Logging') == False: 
				return await c.send('Logging Disabled')
			await c.send('Test Logging Channel')
		else:
			await ctx.send('Logging Channel not set')

	@commands.command()
	async def current_logging(self, ctx):
		await ctx.send('Currently Logging these: {}'.format('0 things' if len(self.settings.ServerConfig(ctx.guild.id, 'LoggingType')) == 0 else ''))
		for l in self.settings.ServerConfig(ctx.guild.id, 'LoggingType'):
			await ctx.send(' - {}'.format(l))

	@commands.command()
	async def setpreset(self, ctx, *, p=None):
		if not p:	
			await ctx.send('Presets available:')
			for l in self.presets:
				await ctx.send(' - {}'.format(l))

			return

		if p in self.presets:
			await ctx.send('Setting Preset to **{}**:'.format(p))
			if p == "all":
				self.settings.ServerConfig(ctx.guild.id, 'LoggingType', self.listeners)
			if p == "basic": 
				self.settings.ServerConfig(ctx.guild.id, 'LoggingType', self.basic)
			if p == "member": 
				self.settings.ServerConfig(ctx.guild.id, 'LoggingType', self.member)
			if p == "advanced_member":
				self.settings.ServerConfig(ctx.guild.id, 'LoggingType', self.advanced_member)
			if p == "message": 
				self.settings.ServerConfig(ctx.guild.id, 'LoggingType', self.message)
			if p == "invite":
				self.settings.ServerConfig(ctx.guild.id, 'LoggingType', self.invite)
			if p == "guild_related":
				self.settings.ServerConfig(ctx.guild.id, 'LoggingType', self.guild_related)
		else:
			await ctx.send('Could\'t find preset: {}'.format(p))
			
	@commands.command()
	async def addpreset(self, ctx, *, preset=None):
		if not p:	
			await ctx.send('Presets available:')
			for l in self.presets:
				await ctx.send(' - {}'.format(l))

			return

		if p in self.presets:
			await ctx.send('Adding Preset **{}** listeners list'.format(p))
			if p == "all":
				self.settings.ServerConfig(ctx.guild.id, 'LoggingType', self.listeners)

			else:
				current_listeners = self.settings.ServerConfig(ctx.guild.id, 'LoggingType')
				if p == "basic": 
					for b in self.basic:
						if not b in current_listeners:
							current_listeners.append(b)
				if p == "member": 
					for b in self.member:
						if not b in current_listeners:
							current_listeners.append(b)
				if p == "advanced_member":
					for b in self.advanced_member:
						if not b in current_listeners:
							current_listeners.append(b)
				if p == "message": 
					for b in self.message:
						if not b in current_listeners:
							current_listeners.append(b)
				if p == "invite":
					for b in self.invite:
						if not b in current_listeners:
							current_listeners.append(b)
				if p == "guild_related":
					for b in self.guild_related:
						if not b in current_listeners:
							current_listeners.append(b)

				self.settings.ServerConfig(ctx.guild.id, 'LoggingType', current_listeners)

	@commands.command()
	async def listpresets(self, ctx, *, p=None):
		"""
		[preset(optional)]
		lists the listers inside preset
		"""
		if not p:	
			await ctx.send('Presets available:')
			for l in self.presets:
				await ctx.send(' - {}'.format(l))

			return
		else:
			if p in self.presets:
				await ctx.send('Presets {}:'.format(p))
				if p == "all":
					for l in self.listeners:
						await ctx.send(' - {}'.format(l))
				if p == "basic": 
					for l in self.basic:
						await ctx.send(' - {}'.format(l))
				if p == "member": 
					for l in self.member:
						await ctx.send(' - {}'.format(l))
				if p == "advanced_member":
					for l in self.advanced_member:
						await ctx.send(' - {}'.format(l))
				if p == "message": 
					for l in self.message:
						await ctx.send(' - {}'.format(l))
				if p == "invite":
					for l in self.invite:
						await ctx.send(' - {}'.format(l))
				if p == "guild_related":
					for l in self.guild_related:
						await ctx.send(' - {}'.format(l))

				return
	
	@commands.command()
	async def listlisteners(self, ctx):
		"""
		guild.chan.delete, guild.chan.update
		"""
		await ctx.send('Listeners available:')
		for l in self.listeners:
			await ctx.send(' - {}'.format(l))

	@commands.command()
	async def addlisteners(self, ctx, *, listener=None):
		"""
		guild.chan.delete, guild.chan.update
		"""
		if not listener:
			await ctx.send('Listeners available:')
			for l in self.listeners:
				await ctx.send(' - {}'.format(l))

			return
			
		l = listener.split(',')
		for listener in l:
			curr_listener = self.settings.ServerConfig(ctx.guild.id, 'LoggingType')
			if listener in self.listeners and not listener in curr_listener:
				curr_listener.append(listener)
				self.settings.ServerConfig(ctx.guild.id, 'LoggingType', curr_listener)
				await ctx.send('Added logging listener: {}'.format(listener))
			else:
				await ctx.send('Could\'t add listener: {}'.format(listener))

	@commands.command()
	async def remlisteners(self, ctx, *, listener=None):
		"""
		guild.chan.delete, guild.chan.update
		"""
		if not listener:
			await ctx.send('Current Listeners currently logging:')
			for l in self.listeners:
				await ctx.send(' - {}'.format(l))

			return

		l = listener.split(',')
		for listener in l:
			curr_listener = self.settings.ServerConfig(ctx.guild.id, 'LoggingType')
			if listener in self.listeners and listener in curr_listener:
				curr_listener.remove(listener)
				self.settings.ServerConfig(ctx.guild.id, 'LoggingType', curr_listener)
				await ctx.send('Now logging listener: {}'.format(listener))
			else:
				await ctx.send('Could\'t add listener: {}'.format(listener))

	@commands.command()
	async def setlisteners(self, ctx, *, listener=None):
		"""
		guild.chan.delete, guild.chan.update
		"""
		if not listener:
			await ctx.send('Listeners available:')
			for l in self.listeners:
				await ctx.send(' - {}'.format(l))

			return

		tmp = []
		l = listener.split(',')
		for listener in l:
			if listener in self.listeners:
				tmp.append(listener)

		self.settings.ServerConfig(ctx.guild.id, 'LoggingType', tmp)
		await ctx("I have set: {} as the current logging listeners".format(tmp))

###########  LISTENERS  ############
	@commands.Cog.listener()
	async def on_bulk_message_delete(self, messages):
		if self.settings.ServerConfig(messages.guild.id, 'Logging') == False: return
		if not 'bulk.msg.delete' in self.settings.ServerConfig(message.guild.id, 'LoggingType'): return

		c = self.bot.get_channel(self.settings.ServerConfig(messages.guild.id, 'LogChannel'))
		if not c: return

		text = "**DELETED MESSAGES**, total: {}".format(len(messages))
		embed=discord.Embed(
			description = text,
			color=0x1fe6b0
		)
		await c.send(embed=embed)
	
	@commands.Cog.listener()
	async def on_guild_channel_delete(self, channel):
		if self.settings.ServerConfig(channel.guild.id, 'Logging') == False: return
		if not 'guild.chan.delete' in self.settings.ServerConfig(channel.guild.id, 'LoggingType'): return

		c = self.bot.get_channel(self.settings.ServerConfig(channel.guild.id, 'LogChannel'))
		if not c: return

		text = "Channel {} deleted".format(channel)
		embed=discord.Embed(
			description = text,
			color=0x1fe6b0
		)
		await c.send(embed=embed)
	
	@commands.Cog.listener()
	async def on_guild_channel_create(self, channel):
		if self.settings.ServerConfig(channel.guild.id, 'Logging') == False: return
		if not 'guild.chan.create' in self.settings.ServerConfig(channel.guild.id, 'LoggingType'): return

		c = self.bot.get_channel(self.settings.ServerConfig(channel.guild.id, 'LogChannel'))
		if not c: return
		
		text = "Channel {} deleted".format(channel)
		embed=discord.Embed(
			description = text,
			color=0x1fe6b0
		)
		await c.send(embed=embed)
	
	@commands.Cog.listener()
	async def on_guild_channel_update(self, before, after):
		if self.settings.ServerConfig(before.guild.id, 'Logging') == False: return
		if not 'guild.chan.update' in self.settings.ServerConfig(before.guild.id, 'LoggingType'): return

		if before.name == after.name: return
		c = self.bot.get_channel(self.settings.ServerConfig(before.guild.id, 'LogChannel'))
		if not c: return
		
		text = f'''**EDITED CHANNEL NAME**```md\n<Before {before.name}>\n ---> \n<After {after.name}>\n```'''
		embed=discord.Embed(
			description = text,
			color=0x1fe6b0
		)
		await c.send(embed=embed)
		
	@commands.Cog.listener()
	async def on_guild_role_create(self, role):
		if self.settings.ServerConfig(role.guild.id, 'Logging') == False: return
		if not 'guild.role.create' in self.settings.ServerConfig(role.guild.id, 'LoggingType'): return

		c = self.bot.get_channel(self.settings.ServerConfig(role.guild.id, 'LogChannel'))
		if not c: return
		
		text = "Role {} Created".format(role.name)
		embed=discord.Embed(
			description = text,
			color=0x1fe6b0
		)
		await c.send(embed=embed)

	@commands.Cog.listener()
	async def on_guild_role_delete(self, role):
		if self.settings.ServerConfig(role.guild.id, 'Logging') == False: return
		if not 'guild.role.delete' in self.settings.ServerConfig(role.guild.id, 'LoggingType'): return

		c = self.bot.get_channel(self.settings.ServerConfig(role.guild.id, 'LogChannel'))
		if not c: return
		
		text = "Role {} deleted".format(role.name)
		embed=discord.Embed(
			description = text,
			color=0x1fe6b0
		)
		await c.send(embed=embed)

	@commands.Cog.listener()
	async def on_guild_role_update(self, before, after):
		if self.settings.ServerConfig(before.guild.id, 'Logging') == False: return
		if not 'guild.role.update' in self.settings.ServerConfig(before.guild.id, 'LoggingType'): return

		if before.name == after.name: return
		c = self.bot.get_channel(self.settings.ServerConfig(before.guild.id, 'LogChannel'))
		if not c: return
		
		text = f'''**EDITED ROLE**```md\n<Before {before.name}> ---> <After {after.name}>\n<Before {before.color}> ---> <After {after.color}>\n```'''
		embed=discord.Embed(
			description = text,
			color=after.color
		)
		await c.send(embed=embed)

	@commands.Cog.listener()
	async def on_member_join(self, member):
		if self.settings.ServerConfig(member.guild.id, 'Logging') == False: return
		if not 'member.join' in self.settings.ServerConfig(member.guild.id, 'LoggingType'): return

		ch = self.bot.get_channel(self.settings.ServerConfig(member.guild.id, 'LogChannel'))	
		if not c: return	

		invite = None
		inv_list = self.invite_list.get(str(member.guild.id), [])
		try:
			new_inv = await member.guild.invites()
		except:
			new_inv = []

		changed = [x for x in new_inv for y in inv_list if x.code == y.code and x.uses != y.uses]
		if len(changed) == 1:
			# Found Invite code
			invite = changed[0]

		self.invite_list[str(member.guild.id)] = new_inv
		
		c = await self.bot.fetch_invite(invite)
		guild = member.guild
		embed=discord.Embed(title="{0}({0.id}) has joined {1}".format(member, guild), color=discord.Color.dark_blue())
		embed.set_thumbnail(url=member.avatar_url)
		embed.add_field(name="Invite URL:", value=c.url, inline=False)
		if c.created_at:
			embed.add_field(name="Created at:", value=c.created_at, inline=True)
		embed.add_field(name="Created By", value=c.inviter, inline=True)
		if c.max_age:	
			embed.add_field(name="Expires:", value=c.max_age, inline=False)
		embed.add_field(name="Pointed to channel:", value=c.channel, inline=True)
		embed.add_field(name="Temporary", value=c.temporary if c.temporary else "False", inline=True)
		embed.add_field(name="For Guild:", value=c.guild, inline=True)
		if c.max_uses != 0 and c.max_uses:
			embed.add_field(name="Uses", value="{}/{}".format(0 if not c.uses else c.uses, c.max_uses), inline=True)
		
		await ch.send(embed=embed)

	@commands.Cog.listener()
	async def on_member_remove(self, member):
		if self.settings.ServerConfig(member.guild.id, 'Logging') == False: return
		if not 'member.remove' in self.settings.ServerConfig(member.guild.id, 'LoggingType'): return

		c = self.bot.get_channel(self.settings.ServerConfig(member.guild.id, 'LogChannel'))
		if not c: return
		
		text = f'**{str(member)}**({str(member.id)}) left **{str(member.guild)}**'
		embed = discord.Embed(
			description = text,
			colour = discord.Color.blue()
		)
		await c.send(embed=embed)

	@commands.Cog.listener()
	async def on_message_edit(self, before, after):
		if not before.guild:
			return

		if self.settings.ServerConfig(before.guild.id, 'Logging') == False: return
		if not 'message.edit' in self.settings.ServerConfig(before.guild.id, 'LoggingType'): return

		if before.content == after.content: return
		c = self.bot.get_channel(self.settings.ServerConfig(before.guild.id, 'LogChannel'))
		if not c: return
		
		text = f'''**EDITED MESSAGE**\n{str(before.author)} ({str(before.author.id)})\nIn channel: {str(before.channel)}\n```md\n<Before {before.content}>\n ---> \n<After {after.content}>\n```'''
		embed=discord.Embed(
			description = text,
			color=discord.Color.orange()
		)
		await c.send(embed=embed)

	@commands.Cog.listener()
	async def on_message_delete(self, message):
		if not message.guild:
			return
			
		if self.settings.ServerConfig(message.guild.id, 'Logging') == False: return
		if not 'message.delete' in self.settings.ServerConfig(message.guild.id, 'LoggingType'): return

		c = self.bot.get_channel(self.settings.ServerConfig(message.guild.id, 'LogChannel'))
		if not c: return
		
		text = f'''**DELETED MESSAGE**\n{str(message.author)} ({str(message.author.id)})\nIn channel: {str(message.channel)}\n```md\n<Deleted: {message.content}>\n```'''
		embed=discord.Embed(
			description = text,
			color=discord.Color.dark_orange()
		)
		await c.send(embed=embed)

	@commands.Cog.listener()
	async def on_member_ban(self, guild, member):
		if self.settings.ServerConfig(guild.id, 'Logging') == False: return
		if not 'message.ban' in self.settings.ServerConfig(guild.id, 'LoggingType'): return

		c = self.bot.get_channel(self.settings.ServerConfig(guild.id, 'LogChannel'))
		if not c: return
		
		text = f'''**BANNED Member**\n{member}({member.id})\n```md\n<Member Banned: {str(member)}>\n```'''
		embed=discord.Embed(
			description = text,
			color=discord.Color.magenta()
		)
		await c.send(embed=embed)

	@commands.Cog.listener()
	async def on_member_unban(self, guild, member):
		if self.settings.ServerConfig(guild.id, 'Logging') == False: return
		if not 'message.unban' in self.settings.ServerConfig(guild.id, 'LoggingType'): return

		c = self.bot.get_channel(self.settings.ServerConfig(guild.id, 'LogChannel'))
		if not c: return
		
		text = f'''**UNBANNED Member**\n{member}({member.id})\n```md\n<Member unBanned: {member}>\n```'''
		embed=discord.Embed(
			description = text,
			color=discord.Color.dark_magenta()
		)
		await c.send(embed=embed)

	@commands.Cog.listener()
	async def on_invite_create(self, invite):
		if self.settings.ServerConfig(invite.guild.id, 'Logging') == False: return
		if not 'invite.create' in self.settings.ServerConfig(invite.guild.id, 'LoggingType'): return

		ch = self.bot.get_channel(self.settings.ServerConfig(invite.guild.id, 'LogChannel'))
		if not ch: return
		
		
		c = invite
		embed=discord.Embed(title=":inbox_tray: Invite created.", color=discord.Color.dark_blue())
		embed.set_thumbnail(url=invite.author.avatar_url)
		embed.add_field(name="Invite URL:", value=c.url, inline=False)
		embed.add_field(name="Created at:", value=c.created_at, inline=True)
		embed.add_field(name="Created By", value=c.inviter, inline=True)
		embed.add_field(name="Expires:", value=c.max_age, inline=False)
		embed.add_field(name="Pointed to channel:", value=c.channel, inline=True)
		embed.add_field(name="Temporary", value=c.temporary if c.temporary else "False", inline=True)
		if c.max_uses != 0:
			embed.add_field(name="Uses", value="{}/{}".format(0 if not c.uses else c.uses, c.max_uses), inline=True)
		await ch.send(embed=embed)

	@commands.Cog.listener()
	async def on_invite_send(self, invite):
		if self.settings.ServerConfig(invite.guild.id, 'Logging') == False: return
		if not 'invite.send' in self.settings.ServerConfig(invite.guild.id, 'LoggingType'): return

		ch = self.bot.get_channel(self.settings.ServerConfig(invite.guild.id, 'LogChannel'))
		if not ch: return
		
		c = invite
		embed=discord.Embed(title=":inbox_tray: Invite sent.", color=discord.Color.dark_green())
		embed.set_thumbnail(url=invite.author.avatar_url)
		embed.add_field(name="Invite URL:", value=c.url, inline=False)
		if c.created_at:
			embed.add_field(name="Created at:", value=c.created_at, inline=True)
		embed.add_field(name="Created By", value=c.inviter, inline=True)
		if c.max_age:	
			embed.add_field(name="Expires:", value=c.max_age, inline=False)
		embed.add_field(name="Pointed to channel:", value=c.channel, inline=True)
		embed.add_field(name="Temporary", value=c.temporary if c.temporary else "False", inline=True)
		if c.max_uses != 0:
			embed.add_field(name="Uses", value="{}/{}".format(0 if not c.uses else c.uses, c.max_uses), inline=True)
		await ch.send(embed=embed)

	@commands.Cog.listener()
	async def on_invite_delete(self, invite):
		if self.settings.ServerConfig(invite.guild.id, 'Logging') == False: return
		if not 'invite.delete' in self.settings.ServerConfig(message.guild.id, 'LoggingType'): return

		ch = self.bot.get_channel(self.settings.ServerConfig(invite.guild.id, 'LogChannel'))
		if not ch: return
		
		c = invite
		embed=discord.Embed(title=":inbox_tray: Invite Deleted.", color=discord.Color.dark_green())
		embed.set_thumbnail(url=invite.author.avatar_url)
		embed.add_field(name="Invite URL:", value=c.url, inline=False)
		if c.created_at:
			embed.add_field(name="Created at:", value=c.created_at, inline=True)
		embed.add_field(name="Created By", value=c.inviter, inline=True)
		if c.max_age:	
			embed.add_field(name="Expires:", value=c.max_age, inline=False)
		embed.add_field(name="Pointed to channel:", value=c.channel, inline=True)
		embed.add_field(name="Temporary", value=c.temporary if c.temporary else "False", inline=True)
		if c.max_uses != 0:
			embed.add_field(name="Uses", value="{}/{}".format(0 if not c.uses else c.uses, c.max_uses), inline=True)
		await ch.send(embed=embed)

	@commands.Cog.listener()
	async def on_member_update(self, before, after):
		if self.settings.ServerConfig(before.guild.id, 'Logging') == False: return
		if not '' in self.settings.ServerConfig(message.guild.id, 'LoggingType'): return

		c = self.bot.get_channel(self.settings.ServerConfig(before.guild.id, 'LogChannel'))
		if not c: return
		
		
		if before.nick != after.nick:
			if 'member.edit.nick' in self.settings.ServerConfig(message.guild.id, 'LoggingType'):
				text = f'''**USER NICKNAME CHANGED**\n{str(before)} ({str(before.id)})\n```md\n<Before {before.nick}>\n ---> \n<After {after.nick}>\n```'''
				embed=discord.Embed(
					description = text,
					color=0xba3ffc
				)
				await c.send(embed=embed)

		if before.name != after.name:
			if 'member.edit.name' in self.settings.ServerConfig(message.guild.id, 'LoggingType'):
				text = f'''**USER NAME CHANGED**\n{str(before)} ({str(before.id)})\n```md\n<Before {before.name}>\n ---> \n<After {after.name}>\n```'''
				embed=discord.Embed(
					description = text,
					color=0x5902d0
				)
				await c.send(embed=embed)

		if before.avatar_url != after.avatar_url:
			if 'member.edit.avatar' in self.settings.ServerConfig(message.guild.id, 'LoggingType'):
				text = f'''**USER AVATAR CHANGED**\n{str(before)} ({str(before.id)})\n```md\n<Before {before.avatar_url}>\n ---> \n<After {after.avatar_url}>\n```'''
				embed=discord.Embed(
					description = text,
					color=0x7612fc
				)
				await c.send(embed=embed)

		if before.activity != after.activity:
			if 'member.edit.activity' in self.settings.ServerConfig(message.guild.id, 'LoggingType'):
				text = f'''**USER ACTIVITY CHANGED**\n{str(before)} ({str(before.id)})\n```md\n<Before {before.activity.name if before.activity else ""}>\n ---> \n<After {after.activity.name if after.activity else ""}>\n```'''
				embed=discord.Embed(
					description = text,
					color=0x47026c
				)
				await c.send(embed=embed)