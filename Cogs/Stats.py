
import discord
from discord.ext import commands

def setup(bot):
	settings = bot.get_cog("Settings")
	bot.add_cog(Stats(bot, settings))

class Stats(commands.Cog):
	def __init__(self, bot, settings):
		self.bot = bot
		self.settings = settings
		#  Notes SLightly Broken

	async def onmemberremove(self, message):
		guild = message.guild
		mem = discord.utils.get(guild.channels, id=self.settings.ServerConfig(guild.id, 'MemStatChannel'))

		try:
			if mem:
				m = 'Member Count: ' + str(len(message.guild.members))
				await mem.edit(name=m)
		except TypeError as e:
			print("Member Count: %s" % e)

	async def onmemberjoin(self, message):
		guild = message.guild
		mem = discord.utils.get(guild.channels, id=self.settings.ServerConfig(guild.id, 'MemStatChannel'))

		try:
			if mem:
				m = 'Member Count: ' + str(len(message.guild.members))
				await mem.edit(name=m)
		except TypeError as e:
			print("Member Count: %s" % e)

	@commands.command()
	async def setmemstat(self, ctx, ch: discord.VoiceChannel = None):
		"""Sets the Channel that will count the amount of members there are in a server"""
		# Sets VC
		# check if channel is used already
		guild = ctx.guild

		if ch:
			if self.settings.ServerConfig(guild.id, 'MemStatChannel') != None:
				if self.settings.ServerConfig(guild.id, 'VcStatChannel') == ch.id:
					return await ctx.send('Channel already in use')

				self.settings.ServerConfig(guild.id, 'MemStatChannel', ch.id)

			await ctx.send('Setting Member Count Stat channel to: **%s**' % ch)

			msg = 'Member Count: ' + str(len(guild.members))
			await ch.edit(name=msg)
		else:
			await ctx.send('Member Count Stat channel removed')
			self.settings.ServerConfig(guild.id, 'MemStatChannel', 0)

	@commands.command()
	async def syncstatchan(self, ctx):
		"""Syncs the stats channels"""
		
		msg = await ctx.send('Resyncing Stat Channels')

		guild = ctx.guild
		mem = self.settings.Get(ctx, 'channel', (self.settings.ServerConfig(guild.id, 'MemStatChannel')))
		
		try:
			if mem:
				m = 'Member Count: ' + str(len(guild.members))
				await mem.edit(name=m)
		except TypeError as e:
			print("Member Count: %s" % e)

		await msg.edit(content='Synced Stat Channels')		