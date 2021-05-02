
import discord
from discord.ext import commands

def setup(bot):
	settings = bot.get_cog("Settings")
	bot.add_cog(Blacklist(bot, settings))

class Blacklist(commands.Cog):
	def __init__(self, bot, settings):
		self.bot = bot
		self.settings = settings

	def randomColor(self):
		return random.choice(self.bot.color)

	@commands.command()
	@commands.is_owner()
	async def RemoveBlackList(self, ctx, server):
		"""[server]
		Removes a server from the blacklist joining"""
		BL = self.BotConfig('BlacklistedServers')
		if int(server) in BL:
			BL.remove(int(server))

		self.BotConfig('BlacklistedServers', BL)
		await ctx.send('Removed {} from Blacklisted servers'.format(server))

	@commands.command()
	@commands.is_owner()
	async def BlackList(self, ctx, server=None): # make check for ID only
		"""[Server]
		Blacklists a server or lists the servers that are blacklisted"""
		_guild = None
		if server:
			for g in self.bot.guilds:
				if g.id == int(server):
					ser = server+'({})'.format(g)
					_guild = g
					break

			await ctx.message.delete()
			con = random.randint(1000, 9999)
			text = f'**Bot Owner {ctx.author.name}({ctx.author.id})**\n```Adding server {ser} to Blacklist```\nConfirm Number:\n`{str(con)}`'
			embed = discord.Embed(
				description = text,
				colour = 0x32a8a6
			)
			msg = await ctx.send(embed=embed)
			user = ctx.message.author
			channel = ctx.message.channel
			time.sleep(0.05)

			def check(m):
				return m.content == str(con) and m.channel == channel and m.author == user

			try:
				t = await self.bot.wait_for('message', timeout=10, check=check)
			except asyncio.exceptions.TimeoutError:
				await msg.delete()
				await ctx.send('Server Blacklist cancelled')
				return

			await msg.delete()
			await t.delete()
			await ctx.send(f'I have Added {server} to the Blacklist')
			BL = self.BotConfig('BlacklistedServers')
			if not server in BL:
				BL.append(int(server))

			if _guild:
				try:
					await _guild.leave()
				except Exception as e:
					print(e)

			self.BotConfig('BlacklistedServers', BL)
		else:
			msg = 'My Blacklisted Servers:'
			for bl in self.BotConfig('BlacklistedServers'):
				msg += '\n - ' + bl

			await ctx.send(msg)