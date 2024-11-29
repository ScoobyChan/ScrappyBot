import json
import random
import discord
from discord.ext import commands
# https://www.piliapp.com/emoticon/lenny-face/


class Lenny(commands.Cog):
	def __init__(self, bot, settings):
		self.bot = bot
		self.settings = settings

	# List Permissions For Bot/Users
	@commands.command()
	async def lenny(self, ctx):
		"""
		Lennys someone
		"""
		lenny = '( ͡° ͜ʖ ͡°)'
		await ctx.message.delete()
		await ctx.send(lenny)

		db_int = self.bot.get_cog("Database_interact")
		if db_int: db_int.update_guild_database_item(ctx.guild.id, "guild_lenny", ctx.author.id)

	# Update JSON
	@commands.command()
	async def lastlenny(self, ctx):
		"""
		Shows who last lennied
		"""
		guild_lenny = user_lenny = user = None
		db_int = self.bot.get_cog("Database_interact")
		if db_int: guild_lenny = db_int.get_guild_database_item(ctx.guild.id, "guild_lenny")

		if guild_lenny: 
			user = self.bot.get_user(guild_lenny)
			user_lenny = user 

		if user_lenny:
			await ctx.send(f"Last Lennied: **{user_lenny}**")
		elif not user:
			await ctx.send('User not found')
		else:
			await ctx.send('No one has Lennied')
	
	@commands.command()
	async def randlenny(self, ctx):
		"""
		Sends a random lenny face
		"""
		ranlenny = ['( ͡° ͜ʖ ͡°)','( ͠° ͟ʖ ͡°)','( ͡~ ͜ʖ ͡°)','( ͡ʘ ͜ʖ ͡ʘ)','( ͡o ͜ʖ ͡o)','(° ͜ʖ °)','( ‾ʖ̫‾)','( ಠ ͜ʖಠ)','( ͡° ʖ̯ ͡°)','( ͡ಥ ͜ʖ ͡ಥ)','༼  ͡° ͜ʖ ͡° ༽','(▀̿Ĺ̯▀̿ ̿)','( ✧≖ ͜ʖ≖)','(ง ͠° ͟ل͜ ͡°)ง',	'(͡ ͡° ͜ つ ͡͡°) ','[̲̅$̲̅(̲̅ ͡° ͜ʖ ͡°̲̅)̲̅$̲̅]','(✿❦ ͜ʖ ❦)','ᕦ( ͡° ͜ʖ ͡°)ᕤ','( ͡° ͜ʖ ͡°)╭∩╮','¯\\_( ͡° ͜ʖ ͡°)_/¯','(╯ ͠° ͟ʖ ͡°)╯┻━┻','( ͡°( ͡° ͜ʖ( ͡° ͜ʖ ͡°)ʖ ͡°) ͡°)','¯\\_(ツ)_/¯','ಠ_ಠ']
		lenny = random.choice(ranlenny)
		await ctx.message.delete()
		await ctx.send(lenny)

		db_int = self.bot.get_cog("Database_interact")
		if db_int: db_int.update_guild_database_item(ctx.guild.id, "guild_lenny", ctx.author.id)


def setup(bot):
	settings = bot.get_cog("Settings")
	bot.add_cog(Lenny(bot, settings))