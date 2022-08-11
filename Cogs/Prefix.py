
import discord
from discord.ext import commands

def setup(bot):
	settings = bot.get_cog("Settings")
	bot.add_cog(Prefix(bot, settings))

class Prefix(commands.Cog):
	def __init__(self, bot, settings):
		self.bot = bot
		self.settings = settings

	def server_owner(ctx):
		return ctx.message.author.id == ctx.guild.owner.id

	@commands.command()
	@commands.check(server_owner)
	async def prefix(self, ctx, *, prefix=None):
		"""[prefix]
		Sets the prefix for the server to a custom one or when empty will display the current prefix"""

		# Server Owner only to change prefix
		guild = ctx.guild.id
		p = self.settings.ServerConfig(guild, 'Prefix')
		if not prefix:
			return await ctx.send('The Prefix for **{}** is: **{}**'.format(ctx.guild.name, p))

		f = self.settings.ServerConfig(guild, 'Prefix', prefix)
		if f == False:
			return

		await ctx.send('Changing Prefix for **{}** from **{}** to **{}**'.format(ctx.guild.name, p, prefix))