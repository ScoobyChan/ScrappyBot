import random
import discord
import requests
from discord.ext import commands
import re
import os
from dotenv import load_dotenv
load_dotenv()

class Honk(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.db_int = self.bot.get_cog("Database_interact")
		self.token = os.getenv("giphy_api_token")

	async def onmessage(self, message):
		if message.author.bot:
			return 	

		if type(message.channel) == discord.DMChannel:
			return

		honk_enable = self.db_int.get_guild_database_item(message.guild.id, "guild_honk_enable", 0)
		honk_guild = self.db_int.get_guild_database_item(message.guild.id, "guild_honk_channel", 0)
		
		if honk_enable == 1:
			if message.channel.id == honk_guild or honk_guild == (0 or None):
				msgs = message.content.lower()
				search_result = re.search("(honk|h.o.n.k|knoh|k.n.o.h)", msgs)
				
				if search_result:
					search = random.choice(['honk', 'goose'])

					if not self.token: return

					API = "http://api.giphy.com/v1/gifs/search?q={}&api_key={}&limit=100&rating=R".format(search, self.token)

					response = requests.get(API)
					data = response.json()
					random_goose = random.choice(data.get("data", None)).get("images", {}).get("downsized", {}).get("url", None)

					await message.channel.send(random_goose)


	@commands.command()
	async def enableHonk(self, ctx):
		"""
		Enables Honk API to post images
		"""
		if self.db_int: 
			guild_honk = self.db_int.get_guild_database_item(ctx.guild.id, "guild_honk_enable", 0)

			if guild_honk == 1:
				self.db_int.update_guild_database_item(ctx.guild.id, "guild_honk_enable", 0)
				await ctx.send('Disabling Honk listener')
			else:
				self.db_int.update_guild_database_item(ctx.guild.id, "guild_honk_enable", 1)	
				await ctx.send('Enabling Honk listener')
		
		else:
			await ctx.send("Unable to connect to database")
	
	@commands.command()
	async def sethonkchannel(self, ctx, name: discord.TextChannel = None):
		"""
		[Channel]
		Adds a dedicated Channel for Honk responses
		"""
		if not name: name = 0
		
		if name == 0:
			self.db_int.update_guild_database_item(ctx.guild.id, "guild_honk_channel", 0)
			await ctx.send('The Honk channel is removed')
		else:	
			self.db_int.update_guild_database_item(ctx.guild.id, 'guild_honk_channel', name.id)
			await ctx.send('The New Honk channel to listen on is: {}'.format(name))

def setup(bot):
	bot.add_cog(Honk(bot))