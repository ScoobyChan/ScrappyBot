
import discord
from discord.ext import commands

def setup(bot):
	settings = bot.get_cog("Settings")
	bot.add_cog(Threads(bot, settings))

class Threads(commands.Cog):
	def __init__(self, bot, settings):
		self.bot = bot
		self.settings = settings

	@commands.command()
	async def thread_join(self, ctx, thread: int):
		thr = self.bot.get_thread(thread)
		await thr.join()

		await ctx.send('I have joined thread {}'.format(thr))
	
	@commands.command()
	async def thread_leave(self, ctx, thread: int):
		thr = self.bot.get_thread(thread)
		await thr.leave()

		await ctx.send('I have left thread {}'.format(thr))
	
	@commands.command()
	async def thread_delete(self, ctx, thread: int):
		thr = self.bot.get_thread(thread)
		await thr.delete()
		await ctx.send('I have Removed thread {}'.format(thr))