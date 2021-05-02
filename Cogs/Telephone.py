import random
import time
import asyncio
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

	@commands.Cog.listener()
	async def on_message(self, message):
		if message.author.bot:
			return

		Sender = 0
		Reciever = 0
		
		for s, r in self.guild_to_guild:
			if message.guild.id == s:
				# print('Reciever:', r)
				Reciever = r
				Sender = s
				break

			if message.guild.id == r:
				# print('Reciever:', s)
				Reciever = s
				Sender = r
				break

		if Reciever == 0:
			return

		if message.content == 'hangup':
			# Alerts Guilds of the ended session
			for g, c in self.calls:
				if Reciever == g:
					channel = self.bot.get_channel(c)
					await channel.send('User has hungup the call')

			for g, c in self.calls:
				if Sender == g:
					channel = self.bot.get_channel(c)
					await channel.send('User has ended the call')
			
			#############################################
			for s, r in self.guild_to_guild:
				if Sender == s or Sender == r or Reciever == s or Reciever == r:
					self.guild_to_guild.remove([s, r])
					
			for s, c in self.calls:
				if Sender == s or Reciever == s:
					self.calls.remove([s, c])

			return
					

		for g, c in self.calls:
			if Reciever == g:
				channel = self.bot.get_channel(c)
				await channel.send('`{}: {}`'.format(message.author.name, message.content))
				break

	@commands.command()
	async def call(self, ctx, number:str = None):
		""""""
		# Find number and call server
		# If none or no answer Time out after 10secs
		#  Check if number is self
		
		if number in self.settings.ServerConfig(ctx.guild.id, 'BlockNumbers'):
			return await ctx.send('**{}** has been blocked by server Administrators'.format(number))

		RecieverGuildID = self.settings.PhoneBook(number)
		SenderGuildID = ctx.guild.id

		if RecieverGuildID == SenderGuildID:
			return await ctx.send('Caller *{}* Busy'.format(number))

		for s, c in self.calls:
			if s == RecieverGuildID:
				return await ctx.send('Caller Busy')

			if s == SenderGuildID:
				return await ctx.send('Server in call already')


		PhoneB = self.settings.PhoneBook()
		SenderNum = ''

		for pb in PhoneB:
			if PhoneB[pb] == SenderGuildID:
				SenderNum = pb
				break

		context = await self.bot.get_context(ctx.message)

		RecieverGuild = self.settings.Get(context, Type='g', Name=RecieverGuildID)
		SenderGuild = self.settings.Get(context, Type='g', Name=SenderGuildID)

		# print(RecieverGuild) #### Works :D
		recieverphonechannel = self.settings.ServerConfig(RecieverGuildID, 'PhoneChannel')
		reciverch = self.bot.get_channel(recieverphonechannel)

		if not RecieverGuild:
			print('missing num')
			return 

		channel = ctx.message.channel
		time.sleep(0.05)

		def check(m):
			return m.content == str('pickup') and m.channel == reciverch

		await ctx.send("Calling **`{}`**".format(number))
		await reciverch.send('*Ring ring...* call incoming from **{}**.  `type pickup to answer`'.format(SenderNum))

		try:
			t = await self.bot.wait_for('message', timeout=10, check=check)
		except asyncio.exceptions.TimeoutError:
			await reciverch.send('Call Missed')
			await ctx.send('Caller didn\'t pick up')
			return

		# Set Servers on call
		self.calls.append([RecieverGuildID, reciverch.id])
		self.calls.append([SenderGuildID, channel.id])
		self.guild_to_guild.append([SenderGuildID, RecieverGuildID])
		await ctx.send('Call in session')
		await reciverch.send('Call in session')

	@commands.command()
	async def phonebook(self, ctx, *, search = None):
		""""""
		phonebook = self.settings.PhoneBook()
		# make it look pretty later
		# Convert ID to Guild

		for p in phonebook:
			await ctx.send('**{}**\n`{}`'.format(phonebook.get(p, None), p))

	@commands.command()
	async def add_to_phone_book(self, ctx, channel: str=None):
		""""""
		if not channel:	
			channel = ctx.channel.id
		channel = self.settings.Get(ctx, 'channel', channel)

		while True:
			numone = str(random.randint(0, 999))
			numtwo = str(random.randint(0, 9999))

			none = "000"
			ntwo = "0000"

			num = "{}{}-{}{}".format(none[:3-len(numone)], numone, ntwo[:4-len(numtwo)], numtwo)
			phonebook = self.settings.PhoneBook(num, ctx.guild.id)
			if phonebook == True:
				phonechannel = self.settings.ServerConfig(ctx.guild.id, 'PhoneChannel', channel.id)
				await ctx.send('Added **{}** to phonebook with number: `{}`'.format(ctx.guild, num))
				break
			elif phonebook == False:
				print(False)
			else:
				# print(phonebook)
				await ctx.send('Server **{}** already in phonebook with number: `{}`'.format(ctx.guild, phonebook[0]))
				break
				
	@commands.command()
	async def rem_num_phone_book(self, ctx):
		"""To complete/fix up"""
		phonechannel = self.settings.ServerConfig(ctx.guild.id, 'PhoneChannel', 0)
		phonebook = self.settings.PhoneBook(num, ctx.guild.id)
		return

	@commands.command()
	async def block(self, ctx, number:str=None):
		"""Blocks the phone number of a server"""
		if not number:
			return

		phonebook = self.settings.PhoneBook()
		if not number in phonebook:
			return await ctx.send('cannot find the number: {}'.format(number))

		blockednum = self.settings.ServerConfig(ctx.guild.id, 'BlockNumbers')
		blockednum.append(number)
		self.settings.ServerConfig(ctx.guild.id, 'BlockNumbers', blockednum)

		await ctx.send("**{}** has been blocked".format(number))
