import discord
from discord.ext import commands

class Nickname(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	# List Permissions For Users
	# @commands.bot_has_permissions(manage_nickname=True, change_nicknames=True)
	@commands.command()
	async def nick(self, ctx, _user: commands.Greedy[discord.Member]=None, *, nName=None):
		"""[user][nickname]
		Nickname user"""
		if not _user: [ctx.author.id]
		
		if not isinstance(_user, list):
			_user = [_user]

		for m in _user:
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
	bot.add_cog(Nickname(bot))