import time
from datetime import datetime
import typing
import discord
from discord.ext import commands

# https://discordpy.readthedocs.io/en/latest/ext/commands/commands.html?highlight=bot%20owner

class JoinDistance:
    def __init__(self, joined, created):
        self.joined = joined
        self.created = created

    @classmethod
    async def convert(cls, ctx, argument):
        member = await commands.MemberConverter().convert(ctx, argument)
        return cls(member.joined_at, member.created_at)

    @property
    def delta(self):
        return self.joined - self.created

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
		readable_format = datetime.fromisoformat(str(member.joined_at)).strftime('%Y-%m-%d %H:%M:%S %Z')

		await ctx.send('{} joined on {}'.format(member, readable_format))
            
	@commands.command()
	async def delta(self, ctx, *, member: JoinDistanceConverter):
		is_new = member.delta.days < 100
		if is_new:
			await ctx.send("Hey you're pretty new!")
		else:
			await ctx.send("Hm you're not so new.")


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