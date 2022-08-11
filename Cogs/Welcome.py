import asyncio
import discord
from discord.ext import commands

def setup(bot):
	settings = bot.get_cog("Settings")
	bot.add_cog(Welcome(bot, settings))

class Welcome(commands.Cog):
	def __init__(self, bot, settings):
		self.bot = bot
		self.settings = settings

	@commands.command()
	async def testwelcome(self, ctx):
		"""Sends a Test Welcome Message to chosen channel"""
		guild = ctx.guild
		ch = discord.utils.get(self.bot.get_all_channels(), id=int(self.settings.ServerConfig(guild.id, 'WelcomeChannel')))
		
		Users = []
		for user in guild.members:
			if str(user.status) != 'offline':
				Users.append(user.name)

		
		if ch == None:
			return await ctx.send('No Welcome channel has been set')

		msg = self.settings.ServerConfig(guild.id, 'WelcomeMsg')
		m = msg.replace('[[user]]', ctx.author.name).replace('[[userID]]', str(ctx.author.id)).replace('[[atuser]]', ctx.author.mention).replace('[[server]]', ctx.guild.name).replace('[[UserCount]]', str(len(ctx.guild.members))).replace('[[online]]', str(len(Users)))
		await ch.send(m)
		
	@commands.command()
	async def testgoodbye(self, ctx):
		"""Sends a Test Welcome Message to chosen channel"""
		guild = ctx.guild
		ch = discord.utils.get(self.bot.get_all_channels(), id=int(self.settings.ServerConfig(guild.id, 'GoodByeChannel')))
		
		Users = []
		for user in guild.members:
			if str(user.status) != 'offline':
				Users.append(user.name)

		if ch == None:
			return await ctx.send('No GoodBye channel has been set')

		msg = self.settings.ServerConfig(guild.id, 'GoodByeMsg')
		m = msg.replace('[[user]]', ctx.author.name).replace('[[userID]]', str(ctx.author.id)).replace('[[atuser]]', ctx.author.mention).replace('[[server]]', ctx.guild.name).replace('[[UserCount]]', str(len(ctx.guild.members))).replace('[[online]]', str(len(Users)))
		await ch.send(m)
		
	@commands.command()
	async def setwelcome(self, ctx, *, msg=None):
		"""
		[welcome Msg]
		This command sets the welcome message

		- [[user]]
		- [[userID]]
		- [[atuser]]
		- [[server]]
		- [[online]]
		- [[UserCount]]
		"""
		guild = ctx.guild

		Users = []
		for user in guild.members:
			if str(user.status) != 'offline':
				Users.append(user.name)

		mess = await ctx.send('Adding Welcome Message..')
		await asyncio.sleep(1)

		if not msg: msg = 'Welcome **[[user]]**([[userID]]) to [[server]]'
		m = msg.replace('[[user]]', ctx.author.name).replace('[[userID]]', str(ctx.author.id)).replace('[[atuser]]', ctx.author.mention).replace('[[server]]', ctx.guild.name).replace('[[UserCount]]', str(len(ctx.guild.members))).replace('[[online]]', str(len(Users)))
		await mess.edit(content='Welcome Message Test: \n\n%s' % m)

		if self.settings.ServerConfig(guild.id, 'WelcomeMsg') != None:
			self.settings.ServerConfig(guild.id, 'WelcomeMsg', m)
		else:
			raise ValueError("Can't find WelcomeMsg in Json")

	@commands.command()
	async def setgoodbye(self, ctx, *, msg=None):
		"""
		[goodbye Msg]
		This command sets the welcome message

		- [[user]]
		- [[userID]]
		- [[server]]
		- [[online]]
		- [[UserCount]]
		"""
		Users = []
		guild = ctx.guild
		for user in guild.members:
			if str(user.status) != 'offline':
				Users.append(user.name)

		mess = await ctx.send('Adding Good bye Message..')
		await asyncio.sleep(1)
		if not msg: msg = '[[user]] has left [[server]]'

		m = msg.replace('[[user]]', ctx.author.name).replace('[[userID]]', str(ctx.author.id)).replace('[[server]]', ctx.guild.name).replace('[[UserCount]]', str(len(ctx.guild.members))).replace('[[online]]', str(len(Users)))
		await mess.edit(content='Good Bye Message Test: \n\n%s' % m)

		if self.settings.ServerConfig(guild.id, 'GoodByeMsg') != None:
			self.settings.ServerConfig(guild.id, 'GoodByeMsg', m)
		else:
			raise ValueError("Can't find GoodByeMsg in Json")

	@commands.command()
	async def setgbyechannel(self, ctx, ch=None):
		"""[channel]
		Sets the channel for good bye. set to 0 for removing it"""
		guild = ctx.guild
		if ch:	
			try:	
				if int(ch) == 0:
					self.settings.ServerConfig(guild.id, 'GoodByeChannel', 0)
			except:
				pass
				
			m = self.settings.Get(ctx, 'channel', ch)
			if not m:
				return await ctx.send('Canno find channel: %s' % ch)
		else:
			m = ctx.channel
		await ctx.send('Setting channel to: **%s**' % m)
		
		if self.settings.ServerConfig(guild.id, 'GoodByeChannel') != None:
			self.settings.ServerConfig(guild.id, 'GoodByeChannel', m.id)
		else:
			raise ValueError("Can't find GoodByeChannel in Json")
	
	@commands.command()
	async def setwelcchannel(self, ctx, ch=None):
		"""[channel]
		Sets the channel for Welcome. set to 0 for removing it"""
		guild = ctx.guild
		if ch:	
			try:	
				if int(ch) == 0:
					self.settings.ServerConfig(guild.id, 'WelcomeChannel', 0)
			except:
				pass

			m = self.settings.Get(ctx, 'channel', ch)
			if not m:
				return await ctx.send('Canno find channel: %s' % ch)
		else:
			m = ctx.channel
		await ctx.send('Setting channel to: **%s**' % m)

		if self.settings.ServerConfig(guild.id, 'WelcomeChannel') != None:
			self.settings.ServerConfig(guild.id, 'WelcomeChannel', m.id)
		else:
			raise ValueError("Can't find GoodByeMsg in Json")