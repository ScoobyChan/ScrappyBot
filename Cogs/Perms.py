import discord
from discord.ext import commands
from discord.ext.commands import MemberConverter

def setup(bot):
	settings = bot.get_cog("Settings")
	bot.add_cog(Perms(bot, settings))

class Perms(commands.Cog):
	def __init__(self, bot, settings):
		self.bot = bot
		self.settings = settings
		self.converter = MemberConverter()

		# Checks for self, Admins, Mods with Admin Override

		@bot.check
		async def audio_perms(ctx):
			# Add DJ role and perms?
			if str(ctx.cog.qualified_name) == 'Music':
				bmember = await MemberConverter().convert(ctx, str(self.bot.user))
				admin = bmember.permissions_in(ctx.channel).administrator

				# Audio
				move = bmember.permissions_in(ctx.channel).move_members
				deafen = bmember.permissions_in(ctx.channel).deafen_members
				speak = bmember.permissions_in(ctx.channel).speak
				connect = bmember.permissions_in(ctx.channel).connect

				if (move and deafen and speak and connect) or admin:
					return True

				else:
					commands.DisabledCommand("""You do not have Connectivity rights
					**Voice Perms** 
					Move members: {}
					Deafen members: {}
					Speak: {}
					Connect: {}

					or for easibility make me administrator
					Is Admin: {}
					""".format(move, deafen, speak, connect))

			else:
				return True

		@bot.check
		async def text_perms(ctx):
			# Checs to see if bot has required text perms and admin perms
			bmember = await MemberConverter().convert(ctx, str(self.bot.user))
			admin = bmember.permissions_in(ctx.channel).administrator

			# Text
			man_mess = bmember.permissions_in(ctx.channel).manage_messages
			add_react = bmember.permissions_in(ctx.channel).add_reactions
			mention = bmember.permissions_in(ctx.channel).mention_everyone
			ext_emotes = bmember.permissions_in(ctx.channel).external_emojis
			att_files = bmember.permissions_in(ctx.channel).attach_files
			embed = bmember.permissions_in(ctx.channel).embed_links
			send = bmember.permissions_in(ctx.channel).send_messages
			read = bmember.permissions_in(ctx.channel).read_messages
			
			member = ctx.author
			
			if (man_mess and add_react and mention and ext_emotes and att_files and embed and send and read) or admin:
				return True
			else:
				text = '''Commands need to be True to work properly:
				**Text Perms**
				Manage Messages: {}
				Add reaction: {}
				Mention Members: {}
				Use external emotes: {}
				attach files: {}
				Send embed: {}
				Send messages: {}
				Read messages: {}

				or for easibility make me administrator
				Is Admin: {}
				'''.format(man_mess, add_react, mention, ext_emotes, att_files, embed, send, read, admin)

				raise commands.DisabledCommand(text)

		@bot.check
		async def requires_special_perms(ctx):
			# Checs to see if bot has required text perms and admin perms
			bmember = await MemberConverter().convert(ctx, str(self.bot.user))
			umember = await MemberConverter().convert(ctx, str(ctx.author))

			admin = bmember.permissions_in(ctx.channel).administrator

			admin_role = self.settings.Get(ctx, 'role', self.settings.ServerConfig(ctx.guild.id, 'AdminRole'))
			
			# Admin
			ban = bmember.permissions_in(ctx.channel).ban_members
			kick = bmember.permissions_in(ctx.channel).kick_members
			man_nick = bmember.permissions_in(ctx.channel).manage_nicknames
			nick = bmember.permissions_in(ctx.channel).change_nickname
			inv = bmember.permissions_in(ctx.channel).create_instant_invite
			man_server = bmember.permissions_in(ctx.channel).manage_guild
			man_web = bmember.permissions_in(ctx.channel).manage_webhooks
			audit = bmember.permissions_in(ctx.channel).view_audit_log
			insight = bmember.permissions_in(ctx.channel).view_guild_insights
			man_emo = bmember.permissions_in(ctx.channel).manage_emojis
			man_role = bmember.permissions_in(ctx.channel).manage_roles
			man_chan = bmember.permissions_in(ctx.channel).manage_channels
			if (str(ctx.command) or str(ctx.cog.qualified_name)) in (self.bot.admin or self.bot.server_owner or self.bot.admin_role or self.bot.kic_ban):
				if (ban and kick and nick and man_nick and inv and man_server and man_web and audit and insight and man_emo and man_role and man_chan) or admin:
					pass
				else:
					raise commands.DisabledCommand("""**Admin Perms**
					Ban members: {}
					Kick members: {}
					Change Nicknames: {}
					Manage Nicknames: {}
					Create invites: {}
					Manage server: {}
					Manage Webhooks: {}
					View audit: {}
					View insight: {}
					Manage Emote: {}
					Manage Roles: {}
					Manage Channels: {}


					or for easibility make me administrator
					Is Admin: {}
					""".format(ban, kick, nick, man_nick, inv, man_server, man_web, audit, insight, man_emo, man_role, man_chan, admin))

				uban = umember.permissions_in(ctx.channel).ban_members
				ukick = umember.permissions_in(ctx.channel).kick_members

				uadmin = umember.permissions_in(ctx.channel).administrator


				####### Run Checks #######
				### Server Commands ###
				if str(ctx.command) in self.bot.server_owner or str(ctx.cog.qualified_name) in self.bot.server_owner:
					if ctx.author.id != ctx.guild.owner_id:
						raise commands.DisabledCommand('You need owner permission to use this command')

				### Admin Commands ###
				if str(ctx.command) in self.bot.admin or str(ctx.cog.qualified_name) in self.bot.admin:
					if not uadmin:
						raise commands.DisabledCommand('You need Admin permissions to use this command')
				
				### Mod commands ###
				if str(ctx.command) in self.bot.admin_role or str(ctx.cog.admin_role) in self.bot.admin_role:
					if not uadmin or not admin_role in ctx.author.roles:
						raise commands.DisabledCommand('You need Moderator Role or Admin perms to use this command')

				### Checks for ban and kick commands ###
				if str(ctx.commands) in self.bot.kic_ban and not ((uban and ukick) or uadmin):
					raise commands.DisabledCommand('User Missing Permissions: Using the command: {} requires both Kick:`{}` and ban: {} to be True or to have admin: `{}`'.format(ctx.command, ukick, uban, uadmin))

			return True

		@bot.check
		async def dis_coms(ctx):
			dis = self.settings.ServerConfig(ctx.guild.id, 'DisabledCommands')
			disOverride = self.settings.ServerConfig(ctx.guild.id, 'DisabledCommandsAdminOverride')
			adminrole = self.settings.Get(ctx, 'role', self.settings.ServerConfig(ctx.guild.id, 'AdminRole'))

			umember = await self.converter.convert(ctx, str(ctx.author))
			is_admin = umember.permissions_in(ctx.channel).administrator
			has_admin_role = True if adminrole in ctx.author.roles else False

			is_server_owner = True if ctx.guild.owner_id == ctx.author.id else False

			if is_server_owner or len(dis) == 0:
				return True

			if disOverride and (has_admin_role or is_admin):
				return True

			if str(ctx.command) in dis or str(ctx.cog.qualified_name) in dis:
				raise commands.DisabledCommand(f'{ctx.command} has been disabled by server owner')

			##### Used for testing purposes ##### 
			# print('Commands: {}'.format(dis))
			# print('Admin Override: {}'.format(disOverride))
			# print('Has Admin role: {}'.format(has_admin_role))
			# print('Is Admin: {}'.format(is_admin))
			# print("Is server owner: {}".format())
			# return True
			###################################### 

		@bot.check
		async def nsfw_coms(ctx):
			Override = self.settings.ServerConfig(ctx.guild.id, 'NSFWOverride')
			if Override:
				return True

			if not str(ctx.command) in self.bot.nsfw or not str(ctx.cog.qualified_name) in self.bot.nsfw:
				return True

			if not ctx.channel.is_nsfw():
				raise commands.DisabledCommand('This requires NSFW permissions')
			
			return True

		### Used for testing purposes
		# @bot.check
		# async def user_perms(ctx):
		# 	bmember = await self.converter.convert(ctx, str(self.bot.user))
		# 	umember = await self.converter.convert(ctx, str(ctx.author))
		
		# 	print("Is Bot owner: {}".format(await self.bot.is_owner(ctx.author)))
		# 	print("Is Bot Administrator: {}".format(bmember.permissions_in(ctx.channel).administrator))
		# 	print("Is server owner: {}".format(self.bot.get_user(ctx.guild.owner_id)))
		# 	print("Is User Administrator: {}".format(umember.permissions_in(ctx.channel).administrator))
		# 	print("Is Bot Kick: {}".format(bmember.permissions_in(ctx.channel).kick_members))
		# 	print(str(ctx.command))
		# 	print(str(ctx.cog.qualified_name))
		# 	return True

	@commands.command()
	@commands.is_owner()
	async def checkbotperm(self, ctx):
		"""Checks the permissions for the Bot Owner only"""
		member = await self.converter.convert(ctx, str(self.bot.get_user(self.bot.user.id)))
		# Bot has Admin Perm
		if member.permissions_in(ctx.channel).administrator == False:
			return await ctx.send('**Bot is missing these permissions:**\n - `Administrator`\n Please make sure bot has these permissions to be able to work properly')
		await ctx.send('Bot has Administrator permissions :)')