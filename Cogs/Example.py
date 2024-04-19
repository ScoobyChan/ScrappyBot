import time
from datetime import datetime
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

		# Format the datetime object to a more readable string format
		readable_format = datetime.fromisoformat(member.joined_at).strftime('%Y-%m-%d %H:%M:%S %Z')

		await ctx.send('{} joined on {}'.format(member, readable_format))

	@commands.command()
	async def slap(self, ctx, members: commands.Greedy[discord.Member], amount:typing.Optional[int] = 1, *, reason='no reason'):
		"""
		Slaps user
		"""
		slapped = ", and ".join(x.name for x in members)
		await ctx.send('{} just got slapped {} times for {}'.format(slapped, amount, reason))

async def setup(bot: commands.Bot) -> None:
	settings = bot.get_cog("Settings")
	await bot.add_cog(Example(bot, settings))