import time
import discord
from discord.ext import commands

class BotAdmin(commands.Cog):
	# print('Fun Cog Working')
	def __init__(self, bot):
		self.bot = bot

	@commands.command()
	async def updatedb(self, ctx):
		"""
		Manual update database
		"""
		int_yaml = self.bot.get_cog("Yaml_interact")
		if int_yaml: int_yaml.check_yaml()
		
		int_json = self.bot.get_cog("Json_interact")
		if int_json: int_json.check_json()

		await ctx.send("Updated databases")

def setup(bot: commands.Bot) -> None:
	bot.add_cog(BotAdmin(bot))