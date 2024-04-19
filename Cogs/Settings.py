import discord
from discord.ext import tasks, commands
from discord.ext.commands import MemberConverter


async def setup(bot: commands.Bot) -> None:
	await bot.add_cog(Settings(bot))

class Settings(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.test = 'test'

	def server_owner(ctx):
		return ctx.message.author.id == ctx.guild.owner_id
