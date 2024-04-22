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
			},
			"User":{},
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

	def save_database(self, new_database):
		# Writing JSON data
		with open(self.filename, 'w') as file:
			json.dump(new_database, file, indent=4)

	def update_item(self):
		loaded_database = self.load_database()
		value = str(self.get_value('item_id'))	

	# Deletes unused DB's - Used for deleting Guilds and Users
	def delete_db(self):
		loaded_database = self.load_database()
		guild_id = str(self.get_value('guild_id'))
		for g in loaded_database:
			if not g in guild_id:
				loaded_database = self.load_database()
				del loaded_database[g]
				self.save_database(loaded_database)
		
	def add_db(self):
		loaded_database = self.load_database()
		# guild_id = str(self.get_value('guild_id'))
  
		value_id = str(self.get_value('item_id'))

		if not loaded_database.get(value_id, None):
			loaded_database[value_id] = self.db[self.database]

		self.save_database(loaded_database)

# Function for updating DB to match config
	def update_db(self):
		# Load Database
		loaded_database = self.load_database()
		current_database_default = self.db[self.database]
		new_database = {}

		value = str(self.get_value('item_id'))

		if value: selected_database = loaded_database.get(value, current_database_default)
		
		for x in current_database_default:
			if not selected_database.get(x, None):
				new_database[x] = current_database_default[x]

		if value:
			loaded_database[value] = new_database
		else:
			loaded_database = new_database

		self.save_database(loaded_database)

	def sync(self):
		# Sync Json to Database
		pass

# Checks to see if Files exists
	def check_db(self):
		if not os.path.exists('database/'): os.mkdir('database') # Create folder if not exists

		if not os.path.exists(f'database/{self.database}.json'):		
			self.save_database({})

class Settings(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.databases = ['Guilds', 'User', 'Bot']

	def server_owner(self, ctx):
		return ctx.message.author.id == ctx.guild.owner_id
	
	def database(self, ctx, action, datab, item_id:str=None, guild_id:list = None, content = None):
		# Check does DB exist

		# Actions:
		actions = ['Delete', 'Update', 'Add', 'Check']

		if not action in actions: return print('Unable to find action')

		# Databases available:
		if not datab in self.databases: return print('Unable to find usable database')

		# Check database
		if action == 'Check': Actions(ctx, datab).check_db(); return
		if action == 'Delete': Actions(ctx, datab, guild_id = guild_id).delete_db(); return
		if action == 'Update': Actions(ctx, datab, item_id = item_id).update_db(); return

		# if datab in ['User', 'Guilds']:
		# 	act = Actions(ctx, datab, item_id = item_id, content = content)
		# else:
		# 	act = Actions(ctx, datab, content = content)

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
			self.database(ctx, 'Check', x)
			if x == "Guilds":
				guild_id = [g.id for g in self.bot.guilds]
				self.database(ctx, 'Delete', x, guild_id=guild_id)
				for g in self.bot.guilds:
					self.database(ctx, 'Update', x, item_id=g.id)
			
			if x == 'User':
				guild_id = [g.id for g in self.bot.users]
				self.database(ctx, 'Delete', x, guild_id=guild_id)
				for u in self.bot.users:
					self.database(ctx, 'Update', x, item_id=u.id)

		await ctx.send('Bot Database updated complete')

