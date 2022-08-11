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

		self.settings.ServerConfig(ctx.guild.id, 'LastLenny', ctx.author.id)


	# Update JSON
	@commands.command()
	async def lastlenny(self, ctx):
		"""
		Shows who last lennied
		"""
		if self.settings.ServerConfig(ctx.guild.id, 'LastLenny') != 0:
			await ctx.send(f"Last Lennied: **{self.settings.ServerConfig(ctx.guild.id, 'LastLenny')}**")
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

		self.settings.ServerConfig(ctx.guild.id, 'LastLenny', ctx.author.id)


def setup(bot):
	settings = bot.get_cog("Settings")
	bot.add_cog(Lenny(bot, settings))