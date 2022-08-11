import json
import discord
from discord.ext import commands

class Suggestion(commands.Cog):
	def __init__(self, bot, settings):
		self.bot = bot
		self.settings = settings

	@commands.command()
	async def Suggestion(self, ctx, *, sug:str=None):
		"""
		[Suggestion]
		sends a suggestion to Server or Bot Owner
		"""
		if not sug:	
			return await ctx.send('No Suggestions given')

		if 	self.settings.BotConfig('SuggestionChannel') != 0:
			ch = self.bot.get_channel(self.settings.BotConfig('SuggestionChannel'))
			if ctx.author.top_role.colour:
				col = ctx.author.top_role.colour
			else:
				col =self.settings.randomColor()

			embed=discord.Embed(title="Suggestion", description=f"{sug}", color=col)
			embed.set_footer(text=f"Server: {ctx.guild}  ||  User: {ctx.author}")
			await ctx.send('I have sent Suggestion')
			await ch.send(embed=embed)
		else:
			await ctx.send('No Suggestion channel found')

	@commands.command()
	async def SetSuggestionChannel(self, ctx, ch=None):
		"""[channel]
		Use Type this in the channel"""

		if not ch:
			ch = ctx.channel

		if ch != 0:	
			ch = self.settings.Get(ctx, 'channel', ch)
			self.settings.BotConfig('SuggestionChannel', ch.id)
		else:
			self.settings.BotConfig('SuggestionChannel', ch)

		await ctx.send('Setting Suggestion Channel to: **' + str(ch) + '**')

	@commands.command()
	async def TestSuggestionChannel(self, ctx):
		"""Use to test the Suggestion channel"""
		ser = self.bot.get_channel(self.settings.BotConfig('SuggestionChannel'))
		if not ser:
			return await ctx.send('Can\'t find Suggestion channel')
			
		await ser.send('Test Suggestion Channel')

def setup(bot):
	settings = bot.get_cog("Settings")
	bot.add_cog(Suggestion(bot, settings))