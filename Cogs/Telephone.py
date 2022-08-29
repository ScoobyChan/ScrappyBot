from email import message
import random
import asyncio
from webbrowser import get
import discord
from discord.ext import commands

# Remove Guild when server leave

def setup(bot):
	settings = bot.get_cog("Settings")
	bot.add_cog(Telephone(bot, settings))

class Telephone(commands.Cog):
	def __init__(self, bot, settings):
		self.bot = bot
		self.settings = settings
		self.calls = []
		self.guild_to_guild = []

		if self.bot.get_cog('Perms'):
			self.bot.admin.append('block')
			self.bot.admin.append('add_to_phone_book')
			self.bot.admin.append('rem_num_phone_book')

	# Requires
	# export phonebook
	# import phonebook

	@commands.Cog.listener()
	async def on_unloaded_extension(self, ext):
		for x in self.guild_to_guild:
			self.guild_to_guild.remove(x)

	async def onmessage(self, message):
		if message.author.bot:
			return
		
		Sender = 0
		Reciever = 0

		user_in_call = None
		for g in self.guild_to_guild:
			if message.guild.id in g:
				user_in_call = g
				break
		
		if not message.channel.id in user_in_call: return; print('Found') # Not a call channel ignore

		ctx = await self.bot.get_context(message)

		if user_in_call[1] == message.channel.id:
			endch = self.bot.get_channel(user_in_call[3])
			getch = self.bot.get_channel(user_in_call[1])
		else:
			endch = self.bot.get_channel(user_in_call[1])
			getch = self.bot.get_channel(user_in_call[3])

		m = await getch.fetch_message(ctx.message.id)

		if m.content == 'hangup': 
			self.guild_to_guild.remove(user_in_call)
			
			await getch.send('Call has ended')
			await endch.send('User has ended the call')
			return

		# Send as webhook
		print(m.author.name)
		print(m.content)
		print(m.author.nick)
		# await endch.send('{}: `{}`'.format(m.author.name if not m.author.name.nick else m.author.name.nick, str(m.content)))
		
		author = m.author.nick or m.author.name
		# await endch.send('{}: `{}`'.format(author, m.content))

		webhook = await endch.create_webhook(name=author)
		await webhook.send(content='```{}```'.format(m.content), avatar_url=m.author.avatar_url)
		await webhook.delete()
		
	@commands.command()
	async def call(self, ctx, number:str = None):
		found_num = self.settings.PhoneBook(ctx.guild.id)
		if not number and found_num:
			return await ctx.send('Servers number is: {}'.format(found_num))

		if not found_num: return await ctx.send('Calling disabled please run: {}enablephone'.format(ctx.prefix))

		if self.settings.PhoneBook(number) in self.settings.ServerConfig(ctx.guild.id, 'BlockNumbers'):
			return await ctx.send('**{}** has been blocked by server Admins'.format(number))

		if not self.settings.PhoneBook(number): return await ctx.send('Unknown number please try again')
		if not self.settings.PhoneBook(ctx.guild.id): return await ctx.send('Calling not setup please contact your Admins')

		RecieverGuildID = self.settings.PhoneBook(number)[0]
		SenderGuildID = ctx.guild.id

		if RecieverGuildID == SenderGuildID:
			return await ctx.send('Caller *{}* Busy'.format(number))

		for s, c in self.calls:
			if s == RecieverGuildID:
				return await ctx.send('Caller Busy')

			if s == SenderGuildID:
				return await ctx.send('Server in call already')

		recguild = self.bot.get_guild(RecieverGuildID)
		reciverch = self.bot.get_channel(self.settings.ServerConfig(RecieverGuildID, 'PhoneChannel'))

		if not recguild:
			await ctx.send('Unable to find server anymore')
			return 

		channel = ctx.message.channel
		await asyncio.sleep(0.05)

		def check(m):
			return m.content == str('pickup') and m.channel == reciverch

		await ctx.send("Calling **`{}`**".format(number))
		await reciverch.send('*Ring ring...* call incoming from **{}**.  \n`type `**pickup**` to answer`'.format(self.settings.PhoneBook(number)[1]))

		try:
			t = await self.bot.wait_for('message', timeout=15, check=check)
		except asyncio.exceptions.TimeoutError:
			await reciverch.send('Call Missed')
			await ctx.send('Caller didn\'t pick up')
			return

		# Set Servers on call
		self.calls.append([RecieverGuildID, reciverch.id])
		self.calls.append([SenderGuildID, channel.id])
		self.guild_to_guild.append([SenderGuildID, channel.id, RecieverGuildID, reciverch.id])
		await ctx.send('Call picked up. Type **hangup** to end')
		await reciverch.send('Call answered. Type **hangup** to end')

	@commands.command()
	async def phonebook(self, ctx, *, search = None):
		phonebook = self.settings.PhoneBook()
		fuz = self.bot.get_cog('FuzzySearch')
		if fuz: 
			if search:
				await fuz.fuzSearch(ctx, search, phonebook)
			else:
				await fuz.fuzList(ctx, phonebook, 'Phone book', max_num = 10)
	
	@commands.command()
	async def enablephone(self, ctx):
		if self.settings.PhoneBook(ctx.guild.id): return await ctx.send('Calling already enabled')
		phonebook = self.settings.PhoneBook()
		
		while True:
			num1 = random.randint(111, 999)
			num2 = random.randint(1111, 9999)

			number = '{}-{}'.format(num1, num2)

			found = False
			for _guild, _number in phonebook:
				if number == _number: found = True
			
			if not found: break

		self.settings.PhoneBook([ctx.guild.id, number], 'add')
		self.settings.ServerConfig(ctx.guild.id, 'PhoneChannel', ctx.message.channel.id)

		await ctx.send('Calling has been setup. Call channel set to: {} and phone number: {}'.format(ctx.message.channel.mention, number))
		
	@commands.command()
	async def chngphonechan(self, ctx, _chan: discord.TextChannel = None):
		phonebook = self.settings.PhoneBook()
		number = found = False

		for _guild, _number in phonebook:
			if ctx.guild.id == _guild: found = True; number = _number; break
		
		if not found: return await ctx.send('Unable to find server in PhoneBook')

		_chan = _chan or ctx.message.channel
		beforech = self.bot.get_channel(self.settings.ServerConfig(ctx.guild.id, 'PhoneChannel'))

		self.settings.ServerConfig(ctx.guild.id, 'PhoneChannel', _chan.id)
		await ctx.send('Old phone channel: {}, New phone channel {}'.format(beforech.mention, _chan.mention))

	@commands.command()
	async def disablephone(self, ctx):
		phonebook = self.settings.PhoneBook(ctx.guild.id)
		
		if not phonebook: return await ctx.send('Unable to find server in PhoneBook')
		
		self.settings.PhoneBook(phonebook, 'del')
		self.settings.ServerConfig(ctx.guild.id, 'PhoneChannel', 0)

		await ctx.send('Calling disabled')

	@commands.command()
	async def blocknum(self, ctx, number):
		found_num = self.settings.PhoneBook(number)
		blocked_num = self.settings.ServerConfig(ctx.guild.id, 'BlockNumbers')
		
		if not found_num: return await ctx.send('Unable to find server')

		if found_num in blocked_num: blocked_num.remove(found_num); await ctx.send('I have removed {} to block list'.format(found_num[1]))
		else: blocked_num.append(found_num); await ctx.send('I have added {} to block list'.format(found_num[1]))
			
	@commands.command()
	async def lockphonechan(self, ctx, _chan: discord.TextChannel = None):
		self.settings.ServerConfig(ctx.guild.id, 'LockPhoneChannel', _chan)
		await ctx.send('Locked channel to {}', _chan if not _chan else _chan.mention)
