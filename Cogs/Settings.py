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
		self.filename = f'database/{self.database}.json'
		self.content = kwargs.items()
		self.db = {
			"Guilds":{
				"shrug":[],
				"lenny":[],
				"testing":2,
				"not_a_test":"maybe"
			},
			"User":{
				"hardware":{}
			},
			"Bot":{}
		}

	def get_value(self, key):
		content_dict = dict(self.content)  # Convert to dictionary
		return content_dict.get(key, None)  # Get the value for the key, with a default fallback

	def load_database(self):
		# Reading JSON data back
		with open(self.filename, 'r') as file:
			loaded_data = json.load(file)

		return loaded_data

	def save_database(self):
		# Writing JSON data
		with open(self.filename, 'w') as file:
			json.dump(self.db[self.database], file, indent=4)

	def update(self):
		pass

	def delete(self):
		pass

	def add(self):
		pass

	def update_db(self):
		# Load Database
		loaded_database = self.load_database()
		
		# Add Missing Items
		for database in self.db:
			for x in self.db[database]:
				if not loaded_database[database].get(x, None):
					loaded_database[database][x] = self.db[database][x]

		self.save_database()
		loaded_database = self.load_database()

		# Delete Missing Items
		for database in loaded_database:
			for x in loaded_database[database]:
				if not  self.db[database].get(x, None):
					del loaded_database[database][x]

		self.save_database()

	def sync(self):
		# Sync Json to Database
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

		if datab in ['User', 'Guilds']:
			act = Actions(ctx, datab, item_id = '', content = '')
		else:
			act = Actions(ctx, datab, _content = '')

		

	@commands.command()
	async def setting_test(self, ctx):
		self.database(ctx, 'Delete', 'User', '181338470520848384 test')
		await ctx.send('Setting Test')

	@commands.command()
	async def setup(self, ctx):
		if not self.server_owner(ctx): return
		await ctx.send('Bot Setup complete on the server')

	@commands.command()
	async def update_db(self, ctx):
		if not self.server_owner(ctx): return
		for x in self.databases:
			self.database(ctx, 'Update', x)
		await ctx.send('Bot Database updated complete')
