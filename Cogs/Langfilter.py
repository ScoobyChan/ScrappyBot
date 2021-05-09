import random
import discord
from discord.ext import commands
from discord.ext.commands import MemberConverter

def setup(bot):
	settings = bot.get_cog("Settings")
	bot.add_cog(Langfilter(bot, settings))

class Langfilter(commands.Cog):
	def __init__(self, bot, settings):
		self.bot = bot
		self.settings = settings

		self.chars = '$#@&!*'

	async def onmemberleave(self, member):
		guild = member.guild
		
		mem = self.settings.ServerConfig(member.guild.id, 'LangFilterUser')
		if mem.get(member.id, None):
			del mem[member.id]
			self.settings.ServerConfig(member.guild.id, 'LangFilterUser', mem)

	async def onmessage(self, message):
		if message.author.id == self.bot.user.id:
			return
			
		if type(message.channel) == discord.DMChannel:
			return

		msg_fixed = str(message.content)
		ctx = await self.bot.get_context(message)

		_filter = self.settings.ServerConfig(message.guild.id, 'LangFilter')
		if '' in _filter: return 
		_filterUser = self.settings.ServerConfig(message.guild.id, 'LangFilterUser')
		_filterWarning = self.settings.ServerConfig(message.guild.id, 'LangFilterWarning')
		_filterKick = self.settings.ServerConfig(message.guild.id, 'LangFilterKick')



		checked = True
		for f in _filter: # change self.filter with DB
			if f in message.content:
				checked = False
				break

		if checked == True:
			return

		if _filterKick != 0:
			if not _filterUser.get(message.author.id, None):
				_filterUser[message.author.id] = 0 
			_filterUser[message.author.id] += 1
			self.settings.ServerConfig(message.guild.id, 'LangFilterUser', _filterUser)

			if _filterUser[message.author.id] == _filterWarning and not _filterWarning == 0:
				await message.channel.send('You have been muted for ten minutes. This is your Warning please stop this behaviour or you will get kicked')
				# Mute for 10 mins


				if self.bot.get_cog("Mute"):
					mute = self.bot.get_cog("Mute")
					ctx = await self.bot.get_context(message)
					await mute._mute(ctx, message.author, message.channel, message.guild)

			if _filterUser[message.author.id] >= _filterKick:
				bmember = await MemberConverter().convert(ctx, str(self.bot.user))
				kick = bmember.permissions_in(ctx.channel).kick_members
				if kick:
					return await message.guild.kick(message.author, reason="Inappropriate behaviour")

				else:
					await ctx.send('User {0}({0.id}) has been using innappropriate language and has exceeded the limit. Please handle them {1}'.format(ctx.author, ctx.guild.owner.mention))

		c = list(self.chars)
		await message.delete()
		for f in _filter: # change self.filter with DB
			if f.lower() in message.content:
				new_word = ''
				for s in range(0, len(f)):
					new_word += random.choice(c)

				msg_fixed = msg_fixed.replace(f.lower(), new_word)

		desc = '**This is not appropriate**({}/{})\n```\n{}\n```'[:2000].format(_filterUser[message.author.id] if _filterKick != 0 else "0", _filterKick, msg_fixed)
		embed=discord.Embed(description=desc)
		await message.channel.send(embed=embed)

	@commands.command()
	async def listlangfilter(self, ctx):
		"""Lists the different items beign filered"""
		_filter = self.settings.ServerConfig(message.guild.id, 'LangFilter')
		desc = "Items being filtered:"
		for f in _filter:
			desc += "\n - `{}`".format(f)

		embed=discord.Embed(description=desc)
		await message.channel.send(embed=embed)

	@commands.command()
	async def addlangfilter(self, ctx, *, arg):
		"""[arg]
		Adds the item to the list that need to be filtered"""
		await ctx.message.delete()

		_filter = self.settings.ServerConfig(ctx.guild.id, 'LangFilter')
		if '' in _filter: _filter = []
		if arg in _filter:
			return await ctx.send('Item already in my list: `{}`'.format(arg))

		_filter.append(arg)
		self.settings.ServerConfig(ctx.guild.id, 'LangFilter', _filter)
		await ctx.send('I have added `{}` to my block list'.format(arg))

	@commands.command()
	async def remlangfilter(self, ctx, *, arg):
		"""[arg]
		 Removes the item to the list that need to be filtered"""
		await ctx.message.delete()

		_filter = self.settings.ServerConfig(ctx.guild.id, 'LangFilter')
		if not arg in _filter:
			return await ctx.send('Item `{}` not in my list'.format(arg))

		_filter.remove(arg)
		if len(_filter) == 0:
			_filter.append('')
			_user = self.settings.ServerConfig(ctx.guild.id, 'LangFilterUser')
			for user in ctx.guild.members:
				_user[user.id] = 0
			self.settings.ServerConfig(ctx.guild.id, 'LangFilterUser', _user)
			
		self.settings.ServerConfig(ctx.guild.id, 'LangFilter', _filter)
		await ctx.send('I have removed `{}` from my block list'.format(arg))

	@commands.command()
	async def dumplangfilter(self, ctx):
		"""Dumps the different files to a file"""
		_filter = self.settings.ServerConfig(ctx.guild.id, 'LangFilter')
		desc = "Items being filtered:"
		for f in _filter:
			desc += "\n - `{}`".format(f)

		f= open(f"langfilter.txt","w+")
		f.write(desc)		
		f.close()

		await ctx.send(file=discord.File(fp="langfilter.txt", filename='langfilter.txt'))

	@commands.command()
	async def clearlangfilter(self, ctx):
		"""Clears the items to filter"""
		self.settings.ServerConfig(ctx.guild.id, 'LangFilter', [''])
		_user = self.settings.ServerConfig(ctx.guild.id, 'LangFilterUser')
		for user in ctx.guild.members:
			_user[user.id] = 0
		self.settings.ServerConfig(ctx.guild.id, 'LangFilterUser', _user)
		await ctx.send('I have cleared the filter list')

	@commands.command()
	async def setlangfilterwarn(self, ctx, warn:int=None):
		# < kick
		_filterWarning = self.settings.ServerConfig(ctx.guild.id, 'LangFilterWarning')
		_filterKick = self.settings.ServerConfig(ctx.guild.id, 'LangFilterKick')

		if not warn:
			return await ctx.send('Cuirrent Warning limit set to: **{}**'.format(_filterWarning))

		if not warn < _filterKick and not warn == 0: return await ctx.send('warning to high. please set one lower than {}'.format(_filterKick))
		self.settings.ServerConfig(ctx.guild.id, 'LangFilterWarning', warn)
		await ctx.send('Setting warning to **{}**'.format(warn if warn != 0 else 'disabled'))

	@commands.command()
	async def setlangfilterkick(self, ctx, kick:int=None):
		# > warn
		_filterWarning = self.settings.ServerConfig(ctx.guild.id, 'LangFilterWarning')
		_filterKick = self.settings.ServerConfig(ctx.guild.id, 'LangFilterKick')
		if not kick:
			return await ctx.send('Cuirrent Warning limit set to: **{}**'.format(_filterKick))
		
		if not kick > _filterWarning and not kick == 0: return await ctx.send('Kick to low')
		self.settings.ServerConfig(ctx.guild.id, 'LangFilterUser', {})
		self.settings.ServerConfig(ctx.guild.id, 'LangFilterKick', kick)
		await ctx.send('Setting kick to **{}**'.format(kick if kick != 0 else 'disabled'))

	@commands.command()
	async def langfilterwarn(self, ctx):
		user = self.settings.ServerConfig(ctx.guild.id, 'LangFilterUser')
		desc = '**Offences:**'
		for u in user:
			_user = await bot.get_user(u)
			desc += "\n{0}({0.id}) offences: {1}".format(_user, user[u])
		await ctx.send(desc)

	@commands.command()
	async def resetlangfilteruser(self, ctx, user: discord.Member=None):
		_user = self.settings.ServerConfig(ctx.guild.id, 'LangFilterUser')
		if not _user.get(user.id, None):
			await ctx.send('Could not find user: {}'.format(user))

		await ctx.send('Removed {} offences'.format(user))
		print(_user)
		_user[user.id] = 0
		print(_user)
		self.settings.ServerConfig(ctx.guild.id, 'LangFilterUser', _user)