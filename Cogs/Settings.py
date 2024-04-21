import os
import json
import discord
from discord.ext import tasks, commands
from discord.ext.commands import MemberConverter


async def setup(bot: commands.Bot) -> None:
	await bot.add_cog(Settings(bot))

class Actions:
	def __init__(self, ctx, database, **kwargs) -> None:
		self.ctx = ctx
		self.database = database
		self.content = kwargs.items()

		self.db = {
			"Guilds":{
				"shrug":[]
			},
			"User":{
				"timezone":""
			},
			"Bot":{}
		}

	def get_value(self, key):
		content_dict = dict(self.content)  # Convert to dictionary
		return content_dict.get(key, None)  # Get the value for the key, with a default fallback

	def update(self):
		pass

	def delete(self):
		pass

	def add(self):
		pass

	def update_db(self):
		pass

	def sync(self):
		pass

	def check_db(self):
		if not os.path.exists('database/'): os.mkdir('database') # Create folder if not exists

		if not os.path.exists(f'database/{self.database}.json'):		
			# Filename to save the data
			filename = f'database/{self.database}.json'

			# Writing JSON data
			with open(filename, 'w') as file:
				json.dump(self.db[self.database], file, indent=4)

class Settings(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.databases = ['Guilds', 'User', 'Bot']

	def server_owner(self, ctx):
		return ctx.message.author.id == ctx.guild.owner_id
	
	def database(self, ctx, action, datab, content = None):
		# Check does DB exist

		# Actions:
		actions = ['Delete', 'Update', 'Add', 'Check']

		if not action in actions: return print('Unable to find action')

		# Databases available:
		if not datab in self.databases: return print('Unable to find usable database')

		# Check database
		if action == 'Check': Actions(ctx, datab).check_db(); return
		if action == 'Update': Actions(ctx, datab).update_db(); return

		if datab == 'User':
			act = Actions(ctx, 'User', _user = '', _content = '')
		else:
			act = Actions(ctx, 'User', _content = '')

		

	@commands.command()
	async def setting_test(self, ctx):
		self.database(ctx, 'Delete', 'User', '181338470520848384 test')
		await ctx.send('Setting Test')

	@commands.command()
	async def setup(self, ctx):
		if not self.server_owner(ctx): return
		for x in self.databases:
			self.database(ctx, 'Check', x)

		await ctx.send('Bot Setup complete on the server')

	@commands.command()
	async def update_db(self, ctx):
		if not self.server_owner(ctx): return
		for x in self.databases:
			self.database(ctx, 'Update', x)

		await ctx.send('Bot Setup complete on the server')
