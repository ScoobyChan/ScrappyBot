import discord
from discord.ext import commands

class Nickname(commands.Cog):
	def __init__(self, bot, settings):
		self.bot = bot
		self.settings = settings

	# List Permissions For Users
	# @commands.bot_has_permissions(manage_nickname=True, change_nicknames=True)
	@commands.command()
	async def nick(self, ctx, user: commands.Greedy[discord.Member]=None, *, nName=None):
		"""[user][nickname]
		Nickname user"""
		if not user:
			user = ctx.author.id

		m = self.settings.Get(ctx, 'user', user)
		await m.edit(nick=nName)
		await ctx.send(str(m.name) + ' Nickname changed to ' + nName)

	@commands.command()
	async def nickall(self, ctx, *, nName=None):
		"""
		[nickname]
		Nick names everyone
		"""
		for m in ctx.guild.members:
			try:	
				await m.edit(nick=nName)
			except Exception as e:
				print(e)
				pass
			
def setup(bot):
	settings = bot.get_cog("Settings")
	bot.add_cog(Nickname(bot, settings))