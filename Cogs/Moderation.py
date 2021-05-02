
import discord
from discord.ext import commands

def setup(bot):
	settings = bot.get_cog("Settings")
	bot.add_cog(Moderation(bot, settings))

class Moderation(commands.Cog):
	def __init__(self, bot, settings):
		self.bot = bot
		self.settings = settings

	def server_owner(ctx):
		return ctx.message.author.id == ctx.guild.owner_id

	@commands.command()
	@commands.is_owner()
	async def botownerlock(self, ctx):
		"""Locks the Bot to Bot owner only"""
		if self.settings.BotConfig('OwnerLock') == True:
			self.settings.BotConfig('OwnerLock', False)
			await ctx.send('Disabling Bot Owner Lock')
		else:
			self.settings.BotConfig('OwnerLock', True)
			await ctx.send('Enabling Bot Owner Lock')

	@commands.command()
	@commands.check(server_owner)
	async def ownerlock(self, ctx): # Server owner
		"""Locks the Bot to server owner only"""
		if self.settings.ServerConfig(ctx.guild.id, 'ServerOwnerLock') == True:
			self.settings.ServerConfig(ctx.guild.id, 'ServerOwnerLock', False)
			await ctx.send('Disabling Server Owner Lock')
		else:
			self.settings.ServerConfig(ctx.guild.id, 'ServerOwnerLock', True)
			await ctx.send('Enabling Server Owner Lock')

	@commands.command()
	@commands.check(server_owner)
	async def adminlock(self, ctx):
		"""Locks the Bot to Admin only"""
		if self.settings.ServerConfig(ctx.guild.id, 'ServerAdminLock') == True:
			self.settings.ServerConfig(ctx.guild.id, 'ServerAdminLock', False)
			await ctx.send('Disabling Admin Lock')
		else:
			self.settings.ServerConfig(ctx.guild.id, 'ServerAdminLock', True)
			await ctx.send('Enabling Admin Lock')

	@commands.command()
	@commands.check(server_owner)
	async def adminrole(self, ctx, *, role=None): # 0 to remove role or blank to list admins
		"""[Role]
		Sets the role for admin/moderators
		make it 0 if you want to reset
		"""
		if not role:
			_role = discord.utils.get(ctx.guild.roles, id=int(self.settings.ServerConfig(ctx.guild.id, 'AdminRole')))
			if _role:
				msg = 'Current Admin Role is: **{}**({})\nUsers with admin role:'.format(_role, _role.id)
				for m in ctx.guild.members:
					for r in m.roles:
						if r.id == _role.id:
							msg += '\n - **' + str(m) + '**(' + str( m.id) + ')'
			else:
				msg = 'Current Admin role is: **{}**'.format(_role)

			await ctx.send(msg)
			return

		try:
			num = discord.utils.get(ctx.guild.roles, id=int(role))
		except ValueError:
			num = discord.utils.get(ctx.guild.roles, name=role)

		if num == None:
			self.settings.ServerConfig(ctx.guild.id, 'AdminRole', 0)
			await ctx.send('Removing the Admin Role')
			return	

		self.settings.ServerConfig(ctx.guild.id, 'AdminRole', num.id)
		await ctx.send('Setting **%s** as the new Admin Role' % num)