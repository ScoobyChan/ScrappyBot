import speedtest
import asyncio
import discord
from discord.ext import commands

def setup(bot):
	settings = bot.get_cog("Settings")
	bot.add_cog(BotComms(bot, settings))

class BotComms(commands.Cog):
	def __init__(self, bot, settings):
		self.bot = bot
		self.settings = settings

	@commands.command()
	@commands.is_owner()
	async def speedtest(self, ctx):
		"""
		Gets the hosts speedtest
		"""
		m = await ctx.send('Running Speed Test... Please wait') 
		try:
			s = speedtest.Speedtest()
			s.get_servers()
			s.get_best_server()
			s.download()
			s.upload()
		except:
			return await ctx.send('Speed test timed out')

		res = s.results.dict()
		t = '**Download: **' + str(int(int(res["download"]) / 1024 / 1024))+'Mbps\n'
		t += '**Upload: **' + str(int(int(res["upload"]) / 1024 / 1024))+'Mbps\n'
		t += '**Ping: **' + str(int(res["ping"]))+'ms'
		await m.edit(content=t)

	@commands.command()
	@commands.is_owner()
	async def botativity(self, ctx, Type, Name, Url=None):
		"""
		[Type of Activity] [Name of Game] [Url(only needed for streaming)]
		This command is used to change the bots activity
		"""
		bot = self.bot.user.id
		b = self.settings.Get(ctx, 'user', bot)
		stat = b.status

		if Type.lower() == 'play':
			game = discord.Activity(name=Name, type=discord.ActivityType.playing)

		if Type.lower() == 'stream':
			if not Url: return await ctx.send('Missing URL')
			game = discord.Activity(name=Name, url=Url, type=discord.ActivityType.streaming)
			
		if Type.lower() == 'watch':
			game = discord.Activity(name=Name, type=discord.ActivityType.watching)
			
		if Type.lower() == 'listen':
			game = discord.Activity(name=Name, type=discord.ActivityType.listening)
			
		await self.bot.change_presence(status=stat, activity=game)

	@commands.command()
	@commands.is_owner()
	async def botstatus(self, ctx):
		"""
		This command is used to set the Bots status using emoji's
		"""
		b = self.server.Get(ctx, 'user', self.bot.user.id)
		game = b.activity

		if game.type == discord.ActivityType.playing:
			game = discord.Activity(name=game.name, type=discord.ActivityType.playing)

		if game.type == discord.ActivityType.streaming:
			game = discord.Activity(name=game.name, url=game.url, type=discord.ActivityType.streaming)
			
		if game.type == discord.ActivityType.watching:
			game = discord.Activity(name=game.name, type=discord.ActivityType.watching)
			
		if game.type == discord.ActivityType.listening:
			game = discord.Activity(name=game.name, type=discord.ActivityType.listening)

		Online = '💚'
		Offline = '🖤'
		Idle = '🧡'
		DnD = '❤️'

		msg = await ctx.send(self.bot.user.name + f" Status:\n```\nOnline: {Online}\nIdle: {Idle}\nDnD: {DnD}\nOffline: {Offline}\n```")
		await msg.add_reaction(Online)
		await msg.add_reaction(Idle)
		await msg.add_reaction(DnD)
		await msg.add_reaction(Offline)

		def check(reaction: discord.Reaction, adder: discord.User) -> bool:
			return adder == ctx.message.author

		try:
			reaction, adder = await self.bot.wait_for('reaction_add', timeout=20, check=check)
		except asyncio.exceptions.TimeoutError:
			await msg.delete()
			await ctx.send('You have not choosen an option')
			return

		await ctx.send(f'Status changed to: {reaction.emoji}')
		await msg.delete()

		if reaction.emoji == Online:
			stat = discord.Status.online
		if reaction.emoji == Offline:
			stat = discord.Status.offline
		if reaction.emoji == DnD:
			stat = discord.Status.dnd
		if reaction.emoji == Idle:		
			stat = discord.Status.idle

		await self.bot.change_presence(status=stat, activity=game)