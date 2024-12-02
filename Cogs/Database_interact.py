import discord
from discord.ext import commands

def setup(bot):
	bot.add_cog(Database_interact(bot))

class Database_interact(commands.Cog):
	def __init__(self, bot):
		self.bot = bot 

####################################################################################################
# mains
####################################################################################################

	def get_database_item(self, db_item, db_return = None):
		Yaml_int = self.bot.get_cog("Yaml_interact")
		Json_int = self.bot.get_cog("Json_interact")
		qet_db_item = db_return
		
		if Json_int or Yaml_int:
			yaml_guild_find = Yaml_int.interact_yaml(db_item)
			json_guild_find = Json_int.interact_json(db_item)

			qet_db_item = yaml_guild_find if yaml_guild_find else json_guild_find

		if qet_db_item: return qet_db_item
		
	def update_database_item(self, db_item, update_item):
		Yaml_int = self.bot.get_cog("Yaml_interact")
		Json_int = self.bot.get_cog("Json_interact")
		qet_db_item = None
		
		if Json_int or Yaml_int:
			yaml_guild_find = Yaml_int.interact_yaml(db_item, data_input=update_item, data_read="w")
			json_guild_find = Json_int.interact_json(db_item, data_input=update_item, data_read="w")

			qet_db_item = yaml_guild_find if yaml_guild_find else json_guild_find

		if qet_db_item: return qet_db_item
		
	def delete_database_item(self, db_item):
		# Work out how this works
		Yaml_int = self.bot.get_cog("Yaml_interact")
		Json_int = self.bot.get_cog("Json_interact")
		qet_db_item = None
		
		if Json_int or Yaml_int:
			yaml_guild_find = Yaml_int.interact_yaml(db_item)
			json_guild_find = Json_int.interact_json(db_item)

			qet_db_item = yaml_guild_find if yaml_guild_find else json_guild_find

		if qet_db_item: return qet_db_item

####################################################################################################
# Guilds
####################################################################################################

	def get_guild_database_item(self, guild_id, db_item, db_return=None):
		Yaml_int = self.bot.get_cog("Yaml_interact")
		Json_int = self.bot.get_cog("Json_interact")
		qet_db_item = db_return
		
		if Json_int or Yaml_int:
			yaml_guild_find = Yaml_int.interact_yaml(db_item)
			json_guild_find = Json_int.interact_json(db_item)

			qet_db_item = yaml_guild_find if yaml_guild_find else json_guild_find

		qet_db_item = qet_db_item.get(str(guild_id), None)
		return qet_db_item
		
	def update_guild_database_item(self, guild_id, db_item, update_item):
		Yaml_int = self.bot.get_cog("Yaml_interact")
		Json_int = self.bot.get_cog("Json_interact")
		
		if Json_int or Yaml_int:
			yaml_guild_find = Yaml_int.interact_yaml(db_item)
			json_guild_find = Json_int.interact_json(db_item)

			updated_db_item = yaml_guild_find if yaml_guild_find else json_guild_find

		updated_db_item[str(guild_id)] = update_item
		
		self.update_database_item(db_item, updated_db_item)
					
		
	def delete_guild_database_item(self, guild_id, db_item):
		# Work out how this works
		Yaml_int = self.bot.get_cog("Yaml_interact")
		Json_int = self.bot.get_cog("Json_interact")
		qet_db_item = None
		
		if Json_int or Yaml_int:
			yaml_guild_find = Yaml_int.interact_yaml(db_item)
			json_guild_find = Json_int.interact_json(db_item)

			qet_db_item = yaml_guild_find if yaml_guild_find else json_guild_find

		if qet_db_item: return qet_db_item