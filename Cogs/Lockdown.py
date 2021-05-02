import asyncio
import discord
from discord.ext import commands

def setup(bot):
	settings = bot.get_cog("Settings")
	bot.add_cog(Lockdown(bot, settings))

class Lockdown(commands.Cog):
	def __init__(self, bot, settings):
		self.bot = bot
		self.settings = settings
		
	@commands.command(name='lockdown')
	async def _lockdown(self, ctx):
		"""
		Add Roles to DB
		Skip Mods and Admin
		Remove Roles
		Remove privalages
		Add privalages to DB
		"""
		lockrole = self.settings.Get(ctx, 'role', self.settings.ServerConfig(ctx.guild.id, 'Lockdown'))
		if lockrole == 0 or not lockrole:
			return await ctx.send('Please run {}makelockrole'.format(ctx.prefix))

		for member in ctx.guild.members:
			if not member.guild_permissions.administrator:
				await member.add_roles(lockrole)

		await ctx.send('Server has been locked down')
		self.settings.ServerConfig(ctx.guild.id, 'isLockedDown', True)

	@commands.command(name='unlock')
	async def _unlockdown(self, ctx):
		"""
		Add Roles to user from DB
		Remove Roles from DB
		Add privalages
		"""
		lockrole = self.settings.Get(ctx, 'role', self.settings.ServerConfig(ctx.guild.id, 'Lockdown'))
		if lockrole == 0 or not lockrole:
			return await ctx.send('Please run {}makelockrole'.format(ctx.prefix))

		for member in ctx.guild.members:
			if not member.guild_permissions.administrator:
				await member.remove_role(lockrole)

		await ctx.send('Server has been unlocked')
		self.settings.ServerConfig(ctx.guild.id, 'isLockedDown', False)

	@commands.command()
	async def makelockrole(self, ctx):
		msg = await ctx.send('Creating Lockdown Role')
		permissions = discord.Permissions.none()
		permissions.read_messages = True
		permissions.read_message_history = True

		lock = await ctx.guild.create_role(name='locked', permissions=permissions)
		self.settings.ServerConfig(ctx.guild.id, 'Lockdown', lock.id)

		for c in ctx.guild.channels:
			await c.set_permissions(lock, read_messages=True, read_message_history=True, connect=False, send_messages=False, speak=False)

		# Add role to channels
		await msg.edit(content='{0.mention} Created, Please set the role above the default role to override permissions'.format(lock))

	@commands.command()
	async def testlock(self, ctx):
		await ctx.send("**Locking Down server for 1 minute**") 
		await ctx.invoke(self._lockdown)
		await asyncio.sleep(60)
		await ctx.invoke(self._unlockdown)
		