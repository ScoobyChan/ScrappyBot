import time
import discord
from discord.ext import commands

class Ping(commands.Cog):
	# print('Fun Cog Working')
	def __init__(self, bot):
		self.bot = bot

	@commands.command()
	async def ping(self, ctx):
		"""
		Ping response
		"""
		t1 = time.perf_counter()
		await ctx.trigger_typing()
		t2 = time.perf_counter()
		ms = round((t2-t1) * 1000)
		await ctx.send(content='**Pong!** <@{}> - {}ms'.format(ctx.author.id, int(ms)))

async def setup(bot: commands.Bot) -> None:
	await bot.add_cog(Ping(bot))