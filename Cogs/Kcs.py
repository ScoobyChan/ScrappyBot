import discord
from discord.ext import commands

def setup(bot):
	settings = bot.get_cog("Settings")
	bot.add_cog(Kcs(bot, settings))

class Kcs(commands.Cog):
	def __init__(self, bot, settings):
		self.bot = bot
		self.settings = settings

	@commands.command()
	async def kcslist(self, ctx):
		kcs = self.settings.KcsConfig(ctx.guild.id)
	
		fuz = self.bot.get_cog('FuzzySearch')
		if fuz: await fuz.fuzList(ctx, kcs, 'KCS list and ID\'s', max_num = 5)

	@commands.command()
	async def addkcs(self, ctx, _id, *, _name):
		self.settings.KcsConfig(ctx.guild.id, _id, _name)

		await ctx.send('Added KCS {}({})'.format(_id, _name))