
import discord
from discord.ext import commands

def setup(bot):
	settings = bot.get_cog("Settings")
	bot.add_cog(Role(bot, settings))

class Role(commands.Cog):
	def __init__(self, bot, settings):
		self.bot = bot
		self.settings = settings

	# Role Selection Menu
	# UwU watch : Emote
	# Speed runners : Emote
	# Among us : Emote


	@commands.command()
	async def roles(self, ctx, *, role=None):
		"""[role(Optional)]
		Lists users in a role if a role is specified or lists the roles in a server"""
		_role = self.settings.Get(ctx, 'role', role)
		desc = ''
		if not _role:
			for r in ctx.guild.roles:
				desc += "\n{}".format(r.mention)

			title = '{} Roles'.format(str(ctx.guild))
		else:
			desc += "<@&{}>".format(str(_role.id))
			for m in ctx.guild.members:
				if _role in m.roles:
					desc += "\n - {}{}".format(m.nick if m.nick else m.name, "({})".format(str(m)) if m.nick else "")

			title = 'Role User List'

		if ctx.author.top_role.colour:
			col = ctx.author.top_role.colour
		else:
			col =self.settings.randomColor()

		embed = discord.Embed(
			title = title,
			description = desc,
			colour = col
		)
		await ctx.send(embed=embed)

	@commands.command()
	async def adduserrole(self, ctx, roleName):
		"""[Role]
		Adds a role to a list that users can use to give themselves roles"""
		_role = self.settings.ServerConfig(ctx.guild.id, 'UserRoles')

		if not roleName:
			return await ctx.send('No role name provided')

		r = self.settings.Get(ctx, 'role', roleName)
		if not r:
			col = self.settings.randomColor()
			r = await ctx.guild.create_role(name=roleName, color=col)

		if not r.id in _role:
			_role.append(r.id)
			self.settings.ServerConfig(ctx.guild.id, 'UserRoles', _role)

		await ctx.send('Adding %s to User roles' % r)

	@commands.command()
	async def remuserrole(self, ctx, roleName):
		"""[Role]
		Removes a role fome a list that users can use to give themselves roles"""
		_role = self.settings.ServerConfig(ctx.guild.id, 'UserRoles')

		if not roleName:
			return await ctx.send('No role name provided')

		r = self.settings.Get(ctx, 'role', roleName)
		if not r:
			return await ctx.send('I can\'t find that role')

		if r.id in _role:
			_role.remove(r.id)
			self.settings.ServerConfig(ctx.guild.id, 'UserRoles', _role)
		await ctx.send('Adding %s to User roles' % r)

	@commands.command()
	async def listuserrole(self, ctx):
		"""Lists all the roles that users can give themselves roles"""
		l = self.settings.LoadSettings()
		text = '**User Roles**'
		for r in self.settings.ServerConfig(ctx.guild.id, 'UserRoles'):
			role = self.settings.Get(ctx, 'role', r)
			text += '\n - <@&{}>'.format(role.id)

		if ctx.author.top_role.colour:
			col = ctx.author.top_role.colour
		else:
			col =self.settings.randomColor()

		embed = discord.Embed(
			description = text,
			colour = col
		)
		await ctx.send(embed=embed)

	@commands.command()
	async def addrole(self, ctx, roleName):
		"""[role]
		Add role that is in the list to user"""
		r = self.settings.Get(ctx, 'role', roleName)
		if not r.id in self.settings.ServerConfig(ctx.guild.id, 'UserRoles'):
			return await ctx.send('This role: **%s** is not one you can add to yourself' % str(r))

		await ctx.author.add_roles(r)
		await ctx.send('I have added the role: **%s** to your roles' % r)

	@commands.command()
	async def remrole(self, ctx, roleName):
		"""[role]
		Removes role from user"""
		r = self.settings.Get(ctx, 'role', roleName)
		if not r.id in self.settings.ServerConfig(ctx.guild.id, 'UserRoles'):
			return await ctx.send('This role: **%s** is not one you can remove from yourself' % str(r))

		await ctx.author.remove_roles(r)
		await ctx.send('I have removed the role: **%s** to your roles' % r)

	@commands.command()
	async def createrole(self, ctx, roleName, col=None):
		"""[role][color(optional)]
		Creates a role for the server
		"""
		r = self.settings.Get(ctx, 'role', roleName)
		if r:
			return await ctx.send("Role already exists")
		
		try:
			if col.startswith('#'):
				col = col.replace('#', '0x')
			val = int(col, 16)
			color=discord.Color(val)
		except ValueError:
			if not col in self.bot.color:
				color = self.settings.randomColor()
			else:
				color = self.bot.color[col]

		r = await ctx.guild.create_role(name=roleName, color=color)
		await ctx.send('I have created the role: **%s**' % roleName)

	@commands.command()
	async def removerole(self, ctx, roleName=None):
		"""
		[RoleName]
		Removes server Role
		"""
		r = self.settings.Get(ctx, 'role', roleName)
		if not r:
			return await ctx.send("Role doesn't exist")
		
		await r.delete()
		await ctx.send('I have deleted the role: **%s**' % r)