import asyncio
import discord
from discord.ext import commands

async def setup(bot):
	await bot.add_cog(Welcome(bot))

class Welcome(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.db_int = self.bot.get_cog("Database_interact")

	@commands.command()
	async def testwelcome(self, ctx):
		"""Sends a Test Welcome Message to chosen channel"""
		if not self.db_int: await ctx.send("Unable to interact with Database") 
		guild = ctx.guild
		Channel = self.db_int.get_guild_database_item(ctx.guild.id, "guild_welcome_channel")
		ch = discord.utils.get(ctx.guild.channels, id=int(Channel))
		
		Users = []
		for user in guild.members:
			if str(user.status) != 'offline':
				Users.append(user.name)

		
		if ch == None:
			return await ctx.send('No Welcome channel has been set')
		
		msg = self.db_int.get_guild_database_item(ctx.guild.id, "guild_welcome_msg")
		if not msg: return await ctx.send("No messages have been set")
		m = msg.replace('[[user]]', ctx.author.name).replace('[[userID]]', str(ctx.author.id)).replace('[[atuser]]', ctx.author.mention).replace('[[server]]', ctx.guild.name).replace('[[UserCount]]', str(len(ctx.guild.members))).replace('[[online]]', str(len(Users)))
		await ch.send(m)
		
	@commands.command()
	async def testgoodbye(self, ctx):
		"""Sends a Test Welcome Message to chosen channel"""
		if not self.db_int: await ctx.send("Unable to interact with Database") 
		guild = ctx.guild
		Channel = self.db_int.get_guild_database_item(ctx.guild.id, "guild_goodbye_channel")
		ch = discord.utils.get(ctx.guild.channels, id=int(Channel))
		
		Users = []
		for user in guild.members:
			if str(user.status) != 'offline':
				Users.append(user.name)

		if ch == None:
			return await ctx.send('No GoodBye channel has been set')

		msg = self.db_int.get_guild_database_item(ctx.guild.id, "guild_goodbye_msg")
		if not msg: return await ctx.send("No messages have been set")
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
		if not self.db_int: await ctx.send("Unable to interact with Database") 
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

		self.db_int.update_guild_database_item(ctx.guild.id, "guild_welcome_msg", m)

	@commands.command()
	async def setgoodbye(self, ctx, *, msg=None):
		if not self.db_int: await ctx.send("Unable to interact with Database") 
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

		self.db_int.update_guild_database_item(ctx.guild.id, "guild_goodbye_msg", m)

	@commands.command()
	async def setgbyechannel(self, ctx, ch=None):
		"""[channel]
		Sets the channel for good bye. set to 0 for removing it"""
		if not self.db_int: await ctx.send("Unable to interact with Database") 
		guild = ctx.guild
		if ch:	
			try:	
				if int(ch) == 0:
					self.db_int.update_guild_database_item(ctx.guild.id, "guild_goodbye_channel", 0)
					return await ctx.send("Set channel to disable")
			except:
				pass
				
			try:
				Name = str(ch).strip('<>#@!&')
				m = discord.utils.get(ctx.guild.channels, id=int(Name))
			except ValueError:
				m = discord.utils.get(ctx.guild.channels, name=Name)

			if not m:
				return await ctx.send('Cannot find channel: %s' % m)
		else:
			m = ctx.channel
		await ctx.send('Setting channel to: **%s**' % m)
		self.db_int.update_guild_database_item(ctx.guild.id, "guild_goodbye_channel", m.id)
		
	
	@commands.command()
	async def setwelcchannel(self, ctx, ch=None):
		"""[channel]
		Sets the channel for Welcome. set to 0 for removing it"""
		if not self.db_int: await ctx.send("Unable to interact with Database") 
		guild = ctx.guild
		if ch:	
			try:	
				if int(ch) == 0:
					self.db_int.update_guild_database_item(ctx.guild.id, "guild_welcome_channel", 0)
					return await ctx.send("Set channel to disable")
			except:
				pass

			try:
				Name = str(ch).strip('<>#@!&')
				m = discord.utils.get(ctx.guild.channels, id=int(Name))
			except ValueError:
				m = discord.utils.get(ctx.guild.channels, name=Name)

			if not m:
				return await ctx.send('Cannot find channel: %s' % m)
		else:
			m = ctx.channel
		await ctx.send('Setting channel to: **%s**' % m)

		self.db_int.update_guild_database_item(ctx.guild.id, "guild_welcome_channel", m.id)