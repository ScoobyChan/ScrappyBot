import random
import discord
from discord.ext import commands

def setup(bot):
	settings = bot.get_cog("Settings")
	bot.add_cog(Langfilter(bot, settings))

class Langfilter(commands.Cog):
	def __init__(self, bot, settings):
		self.bot = bot
		self.settings = settings

		self.chars = '$#@&!'

	async def onmessage(self, message):
		if message.author.id == self.bot.user.id:
			return
			
		if type(message.channel) == discord.DMChannel:
			return

		msg_fixed = str(message.content)
		
		_filter = self.settings.ServerConfig(message.guild.id, 'LangFilter')

		checked = True
		for f in _filter: # change self.filter with DB
			if f in message.content:
				checked = False
				break

		if checked == True:
			return

		c = list(self.chars)
		await message.delete()
		for f in _filter: # change self.filter with DB
			if f.lower() in message.content:
				new_word = ''
				for s in range(0, len(f)):
					new_word += random.choice(c)

				msg_fixed = msg_fixed.replace(f.lower(), new_word)

		desc = '**This is not appropriate**\n```\n{}\n```'[:2000].format(msg_fixed)
		embed=discord.Embed(description=desc)
		await message.channel.send(embed=embed)

	@commands.command()
	async def listlangfilter(self, ctx):
		_filter = self.settings.ServerConfig(message.guild.id, 'LangFilter')
		desc = "Items being filtered:"
		for f in _filter:
			desc += "\n - `{}`".format(f)

		embed=discord.Embed(description=desc)
		await message.channel.send(embed=embed)

	@commands.command()
	async def addlangfilter(self, ctx, *, arg):
		await ctx.message.content.delete()

		_filter = self.settings.ServerConfig(message.guild.id, 'LangFilter')
		if arg in _filter:
			return await ctx.send('Item already in my list: `{}`'.format(arg))

		_filter.append(arg)
		self.settings.ServerConfig(message.guild.id, 'LangFilter', _filter)
		await ctx.send('I have added `{}` to my block list'.format(arg))

	@commands.command()
	async def remlangfilter(self, ctx):
		await ctx.message.content.delete()

		_filter = self.settings.ServerConfig(message.guild.id, 'LangFilter')
		if not arg in _filter:
			return await ctx.send('Item `{}` not in my list'.format(arg))

		_filter.remove(arg)
		self.settings.ServerConfig(message.guild.id, 'LangFilter', _filter)
		await ctx.send('I have removed `{}` from my block list'.format(arg))

	@commands.command()
	async def dumplangfilter(self, ctx):
		_filter = self.settings.ServerConfig(message.guild.id, 'LangFilter')
		desc = "Items being filtered:"
		for f in _filter:
			desc += "\n - `{}`".format(f)

		f= open(f"langfilter.txt","w+")
		f.write(desc)		
		f.close()

		await ctx.send(file=discord.File(fp="langfilter.txt", filename='langfilter.txt'))

	@commands.command()
	async def clearlangfilter(self, ctx):
		self.settings.ServerConfig(message.guild.id, 'LangFilter', [])
		await ctx.send('I have cleared the the language filter list')