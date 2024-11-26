import discord
from discord.ext import commands

class Cool(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.group(pass_context=True)
	async def cool(self, ctx):
		"""Says if a user is cool.
		In reality this just checks if a subcommand is being invoked.
		Usage: $cool bot
		"""
			
		if ctx.invoked_subcommand is None:
			await ctx.send('No, {0.subcommand_passed} is not cool'.format(ctx))

	@cool.command(name='bot')
	async def _bot(self, ctx):
		if await self.settings.perms(ctx)	== (None or False):
			return
			
		await ctx.send('Yes, the bot is cool.')

def setup(bot):
	bot.add_cog(Cool(bot))