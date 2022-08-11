
import discord
from discord.ext import commands

def setup(bot):
	settings = bot.get_cog("Settings")
	bot.add_cog(ServerAdmin(bot, settings))

class ServerAdmin(commands.Cog):
	def __init__(self, bot, settings):
		self.bot = bot
		self.settings = settings

	async def onmemberjoin(self, message):
		guild = message.guild
		_role = self.settings.ServerConfig(guild.id, 'DefaultRole')
		r = discord.utils.get(guild.roles, id=_role)
		
		await message.member.add_roles(r)

	@commands.command()
	async def setdaultchannel(self, ctx, ch: discord.TextChannel = None):
		"""[channel
		Sets the default channel for the server
		Used for sending out notifications"""
		if ch:	
			self.settings.ServerConfig(ctx.guild.id, 'DefaultChannel', ch.id)
			await ctx.send('Setting Default channel to: ' + ch)
		else:
			self.settings.ServerConfig(ctx.guild.id, 'DefaultChannel', 0)
			await ctx.send('Removed Default channel')

	@commands.command()
	async def setdaultrole(self, ctx, roleName: discord.Role=None):
		"""[role]
		Sets default role for the server"""
		if roleName != 0:
			r = self.settings.Get(ctx, 'role', roleName)
			if not r:
				col = self.settings.randomColor()
				r = await ctx.guild.create_role(name=roleName, color=col)

			old = self.settings.Get(ctx, 'role', self.settings.ServerConfig(ctx.guild.id, 'DefaultRole'))

			self.settings.ServerConfig(ctx.guild.id, 'DefaultRole', r.id)
			await ctx.send('Setting DefaultRole to: ' + r)

			for m in ctx.guild.members:
				if not r in m.roles:
					await m.add_roles(r)

			if old:
				for m in ctx.guild.members:
					if old in m.roles:
						m.remove_roles(old)
						
		else:
			self.settings.ServerConfig(ctx.guild.id, 'DefaultRole', discord.utils.get(ctx.guild.roles, name='@everyone'))
			await ctx.send('DefaultRole set to Everyone')

	@commands.command()
	async def setAdminrole(self, ctx, roleName: discord.Role = None):
		"""[Role]
		Sets the Admin Role or if there is none one will be made and the server owner will need to add perms later"""
		if roleName != 0:
			r = self.settings.Get(ctx, 'role', roleName)
			if not r:
				col = self.settings.randomColor()
				r = await ctx.guild.create_role(name=roleName, color=col)

			
			self.settings.ServerConfig(ctx.guild.id, 'AdminRole', r.id)
			await ctx.send('Setting Mod role to: ' + r)
		else:
			self.settings.ServerConfig(ctx.guild.id, 'AdminRole', 0)
			await ctx.send('Removing Mod role')

	@commands.command()
	async def commandChannel(self, ctx, ch: discord.TextChannel = None):
		"""[channel]
		Sets the only channel that all commands can be used in"""
		
		if not ch:
			self.settings.ServerConfig(ctx.guild.id, 'CommandChannel', 0)
			return await ctx.send('Command channel Remove')

		self.settings.ServerConfig(ctx.guild.id, 'CommandChannel', ch.id)
		await ctx.send('Setting Command channel to: ' + ch)