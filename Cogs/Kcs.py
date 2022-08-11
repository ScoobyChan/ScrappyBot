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

		msg = []

		for k in kcs:
			msg.append("{}({})".format(kcs[k]['Name'], k))

		if ctx.author.top_role.colour:
			col = ctx.author.top_role.colour
		else:
			col =self.settings.randomColor()

		embed = discord.Embed(
			title = 'KCS list and ID\'s',
			description = '\n'.join(msg),
			colour = col
		)
		await ctx.send(embed=embed)

	@commands.command()
	async def addkcs(self, ctx, _id, *, _name):
		self.settings.KcsConfig(ctx.guild.id, _id, _name)

		await ctx.send('Added KCS {}({})'.format(_id, _name))