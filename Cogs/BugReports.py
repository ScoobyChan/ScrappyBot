import json
import random
import discord
from discord.ext import commands

class BugReports(commands.Cog):
	def __init__(self, bot, settings):
		self.bot = bot
		self.settings = settings

	# List Permissions For Users
	@commands.command()
	async def BugReport(self, ctx, *, sug:str=None):
		"""
		[Bug to report]
		sends a bug report to Server or Bot Owner
		"""
		if not sug: 
			return await ctx.send('No Bugs given')

		if self.settings.BotConfig('BugreportsChannel') != 0:
			ch = self.bot.get_channel(self.settings.BotConfig('BugreportsChannel'))
			if ctx.author.top_role.colour:
				col = ctx.author.top_role.colour
			else:
				col =self.settings.randomColor()

			embed=discord.Embed(title="Bug found", color=col, description=f"{sug}")
			embed.set_footer(text=f"Server: {ctx.guild}  || User: {ctx.author}")
			await ctx.send('I have sent your Bug to the creator')
			await ch.send(embed=embed)
		else:
			await ctx.send('No Bug channel found')

	@commands.command()
	async def SetBugreportsChannel(self, ctx, ch=None):
		"""[channel]
		Use Type this in the channel"""
		if not ch:
			ch = ctx.channel

		if ch != 0:	
			ch = self.settings.Get(ctx, 'channel', ch)
			self.settings.BotConfig('BugreportsChannel', ch.id)
		else:
			self.settings.BotConfig('BugreportsChannel', ch)

		await ctx.send('Setting Bug Channel to: **' + str(ch) + '**')

	@commands.command()
	async def TestBugChannel(self, ctx):
		"""Use Type this in the channel"""
		ser = self.bot.get_channel(self.settings.BotConfig('BugreportsChannel'))
		if not ser:
			return await ctx.send('Cant find Bug Report channel')
			
		await ser.send('Test Bug Report Channel')


def setup(bot):
	settings = bot.get_cog("Settings")
	bot.add_cog(BugReports(bot, settings))