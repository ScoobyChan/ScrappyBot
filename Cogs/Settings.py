import discord
from discord.ext import tasks, commands
from discord.ext.commands import MemberConverter
import json
import os

async def setup(bot: commands.Bot) -> None:
	await bot.add_cog(Settings(bot))

class Settings(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.test = 'test'

		self.bot.color = [
				discord.Color.teal(), 
				discord.Color.dark_teal(), 
				discord.Color.green(),
				discord.Color.dark_green(),
				discord.Color.blue(),
				discord.Color.dark_blue(),
				discord.Color.purple(),
				discord.Color.dark_purple(),
				discord.Color.magenta(),
				discord.Color.dark_magenta(),
				discord.Color.gold(),
				discord.Color.dark_gold(),
				discord.Color.orange(),
				discord.Color.dark_orange(),
				discord.Color.red(),
				discord.Color.dark_red(),
				discord.Color.lighter_grey(),
				discord.Color.dark_grey(),
				discord.Color.light_grey(),
				discord.Color.darker_grey(),
				discord.Color.blurple(),
				discord.Color.greyple()
		]

		self.settings = {
			"bot_owners": [],
			"bot_admins": [],
			"guild_owner":{},
			"guild_admins":{},
			"blacklisted_guilds":[]
		}

	def server_owner(ctx):
		return ctx.message.author.id == ctx.guild.owner_id

	def check_file(self):
		print(1)
		if not os.path.exists('settings_dict.json'): 
			file = open('settings_dict.json', "w")
			file.write(json.dumps(self.settings))

		print(2)

		# Compare dictionaries
		file = open('settings_dict.json', 'r')
		saved_settings = json.dumps(file.read()) 
		current_settings = json.dumps(self.settings)
		
		if len(current_settings) != len(saved_settings):
			print(3)
			file = open('settings_dict.json', 'w')
			try:
				saved_settings = json.dumps(file.read()) 
			except:
				print(file.read())

			return
			new_setting = {}
			
			for ns in current_settings:
				if ns in saved_settings:
					new_setting[ns] = saved_settings[ns]
				else:
					new_setting[ns] = current_settings[ns]
		
		file.write(json.dumps(new_setting))

		print(4)
		file = open('settings_dict.json', 'r')
		saved_settings = json.dumps(file.read()) 
		return saved_settings

	def load_settings(self):
		settings_dict = self.check_file()

	def save_settings(self):
		settings_dict = self.check_file()

	@commands.command()
	async def test_settings(self, ctx):
		self.load_settings()