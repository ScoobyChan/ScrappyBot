import json
from datetime import tzinfo, timedelta, datetime, date
from pytz import timezone
import asyncio
import pytz
import discord
from async_timeout import timeout
from discord.ext import commands

# Redo to do 1m 1h 1s offsets
# http://pytz.sourceforge.net/#localized-times-and-date-arithmetic

class Time(commands.Cog):
	def __init__(self, bot, settings):
		self.bot = bot
		self.settings = settings

	def search(self, search, re=None, ):
		num = 0
		ls = ''
		for z in pytz.all_timezones:
			if search.lower() in z.lower():
				ls += f"{z}\n"
				num+=1

			if num == 3:
				break
		return ls

	@commands.command()
	async def resettime(self, ctx):
		"""Resets the time for user"""

		# Look for Number 00:00:00
		self.settings.UserConfig(ctx.guild.id, ctx.author.id, 'TimeZone', None)
		await ctx.send(f'Resetting Time Settings for: **{ctx.author.name}**')

	# Look for offset than time zone
	@commands.command()
	async def settime(self, ctx, i=None):
		"""[time]
		sets the time for user"""
			
		# Look for Number (+/-)00:(+/-)00:(+/-)00
		if i:
			t = i.split(':')
			h = t[0]
			if len(h) == 3:
				h = h[1:]

			try:
				h = int(h)
			except:
				pass

			if isinstance(h, int):
				if len(t) == 1:
					i = f'{i}:00:00'
				elif  len(t) == 2:
					i = f'{i}:00'
				else:
					i = f'{i}'

				serID = f'{ctx.guild.id}'
				uID = f'{ctx.author.id}'
				self.settings.UserConfig(ctx.guild.id, ctx.author.id, 'TimeZone', i)
			else:
				if not i in pytz.all_timezones:	
					msg = await ctx.send(f"Results for: **{i}**\n```\n{self.search(i)}\n```")
					await msg.add_reaction("\N{DIGIT ONE}\N{COMBINING ENCLOSING KEYCAP}")
					await msg.add_reaction('\N{DIGIT TWO}\N{COMBINING ENCLOSING KEYCAP}')
					await msg.add_reaction('\N{DIGIT THREE}\N{COMBINING ENCLOSING KEYCAP}')
					await msg.add_reaction('🚫')

					def check(reaction: discord.Reaction, adder: discord.User) -> bool:
						return adder == ctx.message.author and reaction.message.id == msg.id

					reaction = None
					try:
						reaction, adder = await self.bot.wait_for('reaction_add', check=check, timeout=5.0)					
					except:
						pass
						
					if not reaction:
						await msg.delete()
						return await ctx.send('You did not select TimeZone')

					if reaction.emoji == '1⃣':
						choice = 0

					elif reaction.emoji == '2⃣':
						choice = 1

					elif reaction.emoji == '3⃣':
						choice = 2

					t = self.search(i).split('\n')
					i = t[choice]
					await msg.delete()
				
				serID = f'{ctx.guild.id}'
				uID = f'{ctx.author.id}'
				self.settings.UserConfig(ctx.guild.id, ctx.author.id, 'TimeZone', i)
			await ctx.send(f'Setting offset to: **{i}**')
		else:
			await ctx.send(f'Nothing has been set\nFormats:\nTZ: {ctx.prefix}settime Pacific/Auckland\nOffset: {ctx.prefix}settime 01:00:00')

	@commands.command()
	async def searchtz(self, ctx, search=None):
		"""[timezone]
		Searches for a time zone"""
		if not search:
			return await ctx.send('you have not give me anything to search')	
		await ctx.send(f"Search for **{search}** results: \n```\n{self.search(search)}```")
		
	# Look for offset than time zone
	@commands.command()
	async def time(self, ctx, user=None):
		"""[user(optional)]
		Gives time of user or self"""
		if not user:
			uID = f'{ctx.author.id}'
		else:
			m = self.settings.Get(ctx, 'user', user)
			if not m:
				return await ctx.send('Can\'t find the user: %s' % user)
			else:
				uID = m

		# d = timezone('Australia/Sydney')
		j = self.settings.LoadSettings()
		serID = f'{ctx.guild.id}'
		uID = f'{uID}'
		if self.settings.UserConfig(ctx.guild.id, ctx.author.id, 'TimeZone') != None:
			tz = self.settings.UserConfig(ctx.guild.id, ctx.author.id, 'TimeZone')
		else:
			tz = 'UTC'

		t = tz.split(':')
		h = t[0]
		if len(h) == 3:
			h = h[1:]

		try:
			h = int(h)
		except:
			pass

		if isinstance(h, int):
			d = datetime.now(timezone('UTC'))
			d += timedelta(hours=int(t[0]), minutes=int(t[1]), seconds=int(t[2]))
		else:
			d = datetime.now(timezone(tz))
		
		await ctx.send(d.strftime("%a, %d %b %Y %H:%M:%S %p %Z"))

		if self.settings.UserConfig(ctx.guild.id, ctx.author.id, 'TimeZone') == None:	
			await ctx.send(f'User Has not configured TimeZone or Offest please do: `{ctx.prefix}settime [input]`')

def setup(bot):
	settings = bot.get_cog("Settings")
	bot.add_cog(Time(bot, settings))