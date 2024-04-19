import time
import typing
import discord
from discord.ext import commands

# https://discordpy.readthedocs.io/en/latest/ext/commands/commands.html?highlight=bot%20owner

class Example(commands.Cog):
	# print('Fun Cog Working')
	def __init__(self, bot, settings):
		self.bot = bot
		self.settings = settings

	@commands.command()
	async def joined(self, ctx, *, member: discord.Member = None):
		"""
		Joined user
		"""
		if not member: member = ctx.author
		await ctx.send('{0} joined on {0.joined_at}'.format(member))

	@commands.command()
	async def slap(ctx, slapped: discord.Member, amount:typing.Optional[int] = 1, *, reason='no reason'):
		"""
		Slaps user
		"""
		# slapped = ", ".join(x.name for x in members)
		await ctx.send('{} just got slapped {} times for {}'.format(slapped, amount, reason))

async def setup(bot: commands.Bot) -> None:
	settings = bot.get_cog("Settings")
	await bot.add_cog(Example(bot, settings))