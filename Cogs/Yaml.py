
import discord
from discord.ext import commands

def setup(bot):
	settings = bot.get_cog("Settings")
	bot.add_cog(Yaml(bot, settings))

class Yaml(commands.Cog):
	def __init__(self, bot, settings):
		self.bot = bot
		self.settings = settings

	@commands.command(help = "Used for manual Syncing")
	@commands.is_owner()
	async def Sync(self, ctx, serverID=None):
		"""Syncs the JSON files"""
		if serverID:
			# Check if server
			t = False
			for g in self.bot.guilds:
				if g.id == int(serverID):
					t = True

			if t == False:
				return

		msg = await ctx.send('Syncing Json File')
		self.Conf.UpdateJson(serverID)
		await msg.edit(content='Syncing Finished')

	@commands.command()
	@commands.is_owner()
	async def UploadSettings(self, ctx):
		"""Uploads the current json setting to discord"""
		if os.path.exists("Json/"):
			shutil.make_archive("Json/", "zip", "./", "Json")

		if os.path.exists("Json.zip"):
			await ctx.send(file=discord.File(fp="Json.zip", filename=f'Json.zip'))
		else:
			await ctx.send('Can not find the Settings JSON')

	@commands.command()
	@commands.is_owner()
	async def Resetjson(self, ctx):
		"""Resets the json settings to stock"""
		await ctx.message.delete()
		con = random.randint(1000, 9999)
		text = f'**Bot Owner**\n```Reset Json Files```\nConfirm Number:\n`{str(con)}`'
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
			await ctx.send('Reset Json Files cancelled')
			return

		await msg.delete()
		await t.delete()
		
		shutil.rmtree('Json/Users')
		shutil.rmtree('Json/Servers')

		self.Conf.UpdateJson()

		await ctx.send('I have Reset Json Files')

