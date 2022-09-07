
import discord
from discord.ext import commands

def setup(bot):
	settings = bot.get_cog("Settings")
	bot.add_cog(Tts(bot, settings))

class Tts(commands.Cog):
	def __init__(self, bot, settings):
		self.bot = bot
		self.settings = settings

	@commands.command()
	async def pins(self, ctx, channel: discord.TextChannel = None):
		channel = channel or ctx.channel

		pins = [p for p in channel.pins()]
		
		fuz = self.bot.get_cog('FuzzySearch')
		if fuz: 
			await fuz.fuzList(ctx, pins, 'Pins for channel', 25)