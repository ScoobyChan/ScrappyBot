# Used to test subcommands

import discord
from discord.ext import commands

class Cool(commands.Cog):
	def __init__(self, bot, settings):
		self.bot = bot
		self.settings = settings

	@commands.group(pass_context=True)
	async def cool(self, ctx):
		"""Says if a user is cool.
		In reality this just checks if a subcommand is being invoked.
		Usage: $cool bot
		"""
		member = ctx.author

		if ctx.invoked_subcommand is None:
			await ctx.send('No, {} is not cool'.format(member.nick if member.nick else member.name))

	@cool.command(name='bot')
	async def _bot(self, ctx):
		await ctx.send('Yes, the bot is cool.')

async def setup(bot: commands.Bot) -> None:
	settings = bot.get_cog("Settings")
	await bot.add_cog(Cool(bot, settings))