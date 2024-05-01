import json
import random
import discord
from discord.ext import commands
from datetime import datetime
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

		current_datetime = datetime.now()
		formatted_date = current_datetime.strftime('%d-m-%Y %H:%M:%S')
		self.settings.database(ctx, 'Update_Item', 'Guilds', item_id=ctx.guild.id, value_id='lenny', content=[ctx.author.id, str(formatted_date)])


	# Update JSON
	@commands.command()
	async def lastlenny(self, ctx):
		"""
		Shows who last lennied
		"""

		last_lennied = self.settings.database(ctx, 'Get_Item', 'Guilds', item_id=ctx.guild.id, value_id='shrug')
		last_lennied_user = await self.settings.get_username_by_id(ctx, last_lennied[0])
		last_lennied_time = last_lennied[1]
		# print(last_lennied)
		if last_lennied:
			await ctx.send(f"**{last_lennied_user}** Last Lennied on **{last_lennied_time}**") # Convert Time to TZ, convert User ID to Username/Nick
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

		current_datetime = datetime.now()
		formatted_date = current_datetime.strftime('%d-m-%Y %H:%M:%S')
		self.settings.database(ctx, 'Update_Item', 'Guilds', item_id=ctx.guild.id, value_id='lenny', content=[ctx.author.id, str(formatted_date)])



async def setup(bot: commands.Bot) -> None:
	settings = bot.get_cog("Settings")
	await bot.add_cog(Lenny(bot, settings))