import discord
from discord.ext import tasks, commands
from discord.ext.commands import MemberConverter


async def setup(bot: commands.Bot) -> None:
	await bot.add_cog(Settings(bot))

class Settings(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.test = 'test'

		self.bot.color = [
				discord.Color.teal(), 
				discord.Color.dark_teal(), 
				discord.Color.green(),
				discord.Color.dark_green(),
				discord.Color.blue(),
				discord.Color.dark_blue(),
				discord.Color.purple(),
				discord.Color.dark_purple(),
				discord.Color.magenta(),
				discord.Color.dark_magenta(),
				discord.Color.gold(),
				discord.Color.dark_gold(),
				discord.Color.orange(),
				discord.Color.dark_orange(),
				discord.Color.red(),
				discord.Color.dark_red(),
				discord.Color.lighter_grey(),
				discord.Color.dark_grey(),
				discord.Color.light_grey(),
				discord.Color.darker_grey(),
				discord.Color.blurple(),
				discord.Color.greyple()
		]

	def server_owner(ctx):
		return ctx.message.author.id == ctx.guild.owner_id
