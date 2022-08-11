import asyncio
import time
import discord
from discord.ext import commands

def setup(bot):
	settings = bot.get_cog("Settings")
	bot.add_cog(Buttons(bot, settings))

class Buttons(commands.Cog):
	def __init__(self, bot, settings):
		self.bot = bot
		self.settings = settings

	@commands.command()
	async def button(self, ctx):
		""""Button testing"""
		test = ['test1', 'test2', 'test3', 'test4', 'test5', 'test6', 'test7']
		

	def viewing_list(self, ctx, _list_input):
		self.emoji_to_role = [
            discord.PartialEmoji(name='➡️'),  # ID of the role associated with unicode emoji '🔴'.
            discord.PartialEmoji(name='⬅️'),  # ID of the role associated with unicode emoji '🟡'.
            discord.PartialEmoji(name='🚫'),  # ID of the role associated with a partial emoji's ID.
        ]

		start_list = 0
		end = len(_list_input) - 1
		max_display = end_list = 5

		# press button increase
		# press button decrease

		if end > max_display:
			print(_list_input[start_list:end_list])
			
			start_list += 5
			end_list += 5

			print(_list_input[start_list:end_list])
			
			print(end_list)
			start_list += 5
			end_list += 5

			if len(_list_input[start_list:end_list]) == 0:
				print('Empty')
				start_list -= 5
				end_list -= 5

			if start_list < 0: 
				start_list = 0
				end_list = max_display
			
			print(_list_input[start_list:end_list])
