import time
import typing
import discord
from discord.ext import commands

# https://discordpy.readthedocs.io/en/latest/ext/commands/commands.html?highlight=bot%20owner

class Example(commands.Cog):
	# print('Fun Cog Working')
	def __init__(self, bot):
		self.bot = bot

	@commands.command()
	async def joined(self, ctx, *, member: discord.Member = None):
		"""
		Joined user
		"""
		if not member: member = ctx.author
		await ctx.send('{0} joined on {0.joined_at}'.format(member))

	# @commands.command()
	# async def slap(ctx, members: commands.Greedy[discord.Member] = None, amount:typing.Optional[int] = 1, *, reason='no reason'):
	# 	"""
	# 	Slaps user
	# 	"""
	# 	if members: 
	# 		slapped = ", ".join(x.name for x in members)
	# 	else:
	# 		members = ctx.author.name
	# 	await ctx.send('{} just got slapped {} times for {}'.format(slapped, amount, reason))

def setup(bot):
	bot.add_cog(Example(bot))