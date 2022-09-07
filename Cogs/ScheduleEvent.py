
import discord
from discord.ext import commands

def setup(bot):
	settings = bot.get_cog("Settings")
	bot.add_cog(ScheduleEvent(bot, settings))

class ScheduleEvent(commands.Cog):
	def __init__(self, bot, settings):
		self.bot = bot
		self.settings = settings

	@commands.command()
	async def start_event(self, ctx, event_id: int, *, reason = None):
		event = self.bot.get_scheduled_event(event_id)
		await event.start(reason)
		await ctx.send('Started event: {}'.format(event))

	@commands.command()
	async def stop_event(self, ctx, event_id: int, *, reason = None):
		event = self.bot.get_scheduled_event(event_id)
		await event.end(reason)
		await ctx.send('Stop event: {}'.format(event))

	@commands.command()
	async def cancel_event(self, ctx, event_id: int, *, reason = None):
		event = self.bot.get_scheduled_event(event_id)
		await event.cancel(reason)
		await ctx.send('Cancelled event: {}'.format(event))

	@commands.command()
	async def delete_event(self, ctx, event_id: int, *, reason = None):
		event = self.bot.get_scheduled_event(event_id)
		await event.delete(reason)
		await ctx.send('Deleted event: {}'.format(event))
