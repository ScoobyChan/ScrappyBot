import os
import json
import asyncio
import discord
from discord.ext import commands

def setup(bot):
	settings = bot.get_cog("Settings")
	bot.add_cog(BotControl(bot, settings))

class BotControl(commands.Cog):
	def __init__(self, bot, settings):
		self.bot = bot
		self.settings = settings

	@commands.command()
	@commands.is_owner()
	async def reboot(self, ctx):
		"""Reboots the bot - Bot Owner only"""
		# Need to re do
		t = await ctx.channel.send('Rebooting Bot')
		# CogLoader
		await asyncio.sleep(0.5)
		await t.edit(content='Unloading Cog loader')
		cg_load = self.bot.get_cog('CogLoader')
		if not cg_load == None:
			await asyncio.sleep(0.5)
			await t.edit(content='Unloading cogs')
			cg_load._unload_extension()
			await asyncio.sleep(0.5)
			await t.edit(content='Unloading Cog loader')
			self.bot.unload_extension("Cogs.CogLoader")

		# Settings
		await asyncio.sleep(0.5)
		await t.edit(content='Unloading Settings')
		set_load =self. bot.get_cog('Settings')
		if not set_load == None:	
			await asyncio.sleep(0.5)
			await t.edit(content='Unloading Settings Cog')
			self.bot.unload_extension("Cogs.Settings")

		print('Rebooting')
		await asyncio.sleep(5)
		os.system('Python3 Bot.py')
		await self.bot.logout()

	@commands.command()
	@commands.is_owner()
	async def shutdown(self, ctx):
		# Need to redo
		"""Shuts down the bot - Bot Owner only"""
		t = await ctx.channel.send('Shutting down Bot')

		cg_load = self.bot.get_cog('CogLoader')
		if not cg_load == None:
			await asyncio.sleep(0.5)
			await t.edit(content='Unloading cogs')
			cg_load._unload_extension()
			await asyncio.sleep(0.5)
			await t.edit(content='Unloading Cog loader')
			self.bot.unload_extension("Cogs.CogLoader")

		# Settings
		set_load = self.bot.get_cog('Settings')
		if not set_load == None:	
			await asyncio.sleep(0.5)
			await t.edit(content='Unloading Settings Cog')
			self.bot.unload_extension("Cogs.Settings")

		await t.edit(content="Good bye **{}**".format(ctx.author))
		await asyncio.sleep(5)
		await self.bot.logout()
		exit(0)
