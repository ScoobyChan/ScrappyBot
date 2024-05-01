import json
import codecs
import base64
import discord
from discord.ext import commands


class Encode(commands.Cog):
	def __init__(self, bot, settings):
		self.bot = bot
		self.settings = settings

	# List Permissions For Bot/Users
	@commands.command()
	async def encode(self, ctx, From=None, To=None, *, msg:str=None):
		# may need to fix later
		"""
		[From] [To] [What needs encoding]
		Encodes/decodes messages
		"""
		c = ['a', 'b', 'h', 'u']
		if not From or not To or not msg:
			await ctx.send(f'Usage: `{ctx.prefix}encode b a to_encode`')
			await ctx.send(f'Languages: Basex64(b), Hexidecimal(h), Unicode(u) and ASCII(a)')
			return

		if From == To:
			return await ctx.send('Encoding to and from same')

		if not From in c and not To in c:
			return await ctx.send('From and/or the To encode isn\'t right please make sure its the single letter (b, h, u, a)')

		# Converts all to ASCII
		try:
			if From == 'b':
				try:	
					t = codecs.decode(msg.encode('utf-8'), "base64").decode('ascii')
				except:
					t = codecs.decode(msg.encode('utf-8'), "base64")
				F = 'Base64'
			elif From == 'a':
				t = codecs.decode(msg.encode('utf-8'), 'ascii')
				F = 'ASCII'
			elif From == 'h':
				t = codecs.decode(msg.encode('utf-8'), "hex").decode('ascii')
				F = 'Hexidecimal'
			elif From == 'u' and To == 'a':
				F = 'Unicode'
				pass
			else:
				print('Invalid')
				return 

		except Exception as e:
			if "decoding with 'hex' codec failed (Error: Odd-length string)" == str(e):
				await ctx.send('Not a valid **hex Value**')
				return

			if "decoding with 'base64' codec failed (Error: Invalid base64-encoded string: number of data characters (5) cannot be 1 more than a multiple of 4)" == str(e):
				await ctx.send('Not a valid **base64 Value**')
				return

			print(e)
			return

		# Convert to Non Ascii
		try:
			if To == 'b':
				t = codecs.encode(t.encode('utf-8'), 'base64').decode('ascii')
				T = 'Base64'
			elif To == 'a':
				T = 'ASCII'
				pass
			elif To == 'h':
				t = codecs.encode(t.encode('utf-8'), 'hex').decode('ascii')
				T = 'Hexidecimal'
			elif To == 'u':
				t = t.encode('unicode-escape').decode('ascii')
				T = 'Unicode'

		except Exception as e:
			print(e)
			return

		# await ctx.send(f'**{F}** to **{T}**\n```{t}```')

		if ctx.author.top_role.colour:
			col = ctx.author.top_role.colour
		else:
			col =self.server.randomColor()

		embed = discord.Embed(
			description = f'**{F}** to **{T}**\n```{t}```',
			colour = col
		)
		await ctx.send(embed=embed)

async def setup(bot: commands.Bot) -> None:
	settings = bot.get_cog("Settings")
	await bot.add_cog(Encode(bot, settings))