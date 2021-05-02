import socket
import discord
import asyncio
from discord.ext import commands
from mcstatus import MinecraftServer

class Minecraft(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		
	# Add restart
	# Mine to discord
	# Save Server to Bot settings
	
	@commands.command()
	async def ip(self, ctx):
		"""
		Sends the IP address for MC
		"""

		if ctx.author.top_role.colour:
			col = ctx.author.top_role.colour
		else:
			col =self.settings.randomColor()

		embed = discord.Embed(
			title = 'Minecraft IP',
			description = 'IP Address: **{}**'.format(self.bot.minecraft),
			colour =col
		)

	@commands.command()
	async def mcstat(self, ctx):
		"""
		Sends status of MC server
		"""

		# print('Minecraft')
		host_name = socket.gethostname()
		host_ip = socket.gethostbyname(host_name)

		# host_ip = '192.168.1.254'
		server = MinecraftServer.lookup("{}:25565".format(host_ip))
		try:
			status = server.status()
			stats = '```md\n[Archimous Server][The server has {0} players and replied in {1} ms]\n```'.format(status.players.online, status.latency)
		except:
			print('Server closed')
			stats = '```md\n[Archimous Server][The server is closed ATM for Maintainance]\n```'

		await ctx.send(stats)
		
	@commands.command()
	async def SBS(self, ctx):
		"""
		Should start the server through discord
		"""
		msg = await ctx.send('Starting Archimous Server...')
		await asyncio.sleep(1)
		await msg.edit(content='eee')
		await asyncio.sleep(3)
		await msg.edit(content='eee rrr')
		await asyncio.sleep(3)
		await msg.edit(content='eee rrr eee')
		await asyncio.sleep(3)
		await msg.edit(content='eee rrr eee reerrer')
		await asyncio.sleep(3)
		await msg.edit(content='Server Loaded')
		await asyncio.sleep(15)
		await msg.edit(content='LOL, This command would start Archimous Server if it was Operational 😎\nAnother Day perhaps')

def setup(bot):
	bot.add_cog(Minecraft(bot))