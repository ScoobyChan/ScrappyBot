# Credits CorpNewt for 
# https://github.com/corpnewt/CorpBot.py/blob/bc5c08e848a766d5c75920352b0a09bc4c04c2b2/Cogs/Actions.py

import random
import discord
from discord.ext import commands
from Utils import Member
from Utils import Computer

class Bonk(commands.Cog):
	def __init__(self, bot, settings):
		"""Credits to CorpNewt for Computer and Member"""
		self.bot = bot
		self.settings = settings

	@commands.command()
	async def bonk(self, ctx, member=None):
		"""
		[object]
		Spooks and object
		"""

		Bot = self.bot.user.id
		M = Member.member()
		C = Computer.computer()

		nothingList = [ 'you Bonk no one but yourself']

		botList = [ 	'you Bonked me why? I am a robot you can not bonk me mortal so I bonk you!']

		selfList = [	'you\'re gonna need a bigger bat to bonk yourself!']

		memberList = [  'you Bonk *{}* so hard that they become flat headed!']
		
		itemList = [	'you Bonk *{}* with no reaction, leaving you looking weird...']

		if member:
			m = M.displayName(ctx, member)
			print(m)
			if m == None:
				msg = C.text(ctx, itemList, member)
			elif m.id == Bot:
				msg = C.text(ctx, botList, m.name)
			elif m.id == ctx.author.id:
				msg = C.text(ctx, selfList, m.name)
			else:
				msg = C.text(ctx, memberList, m.name)
		else:
			msg = C.text(ctx, nothingList)

		# print(msg)	
		await ctx.send(msg)
		await ctx.send("https://tenor.com/view/kendo-shinai-bonk-doge-horny-gif-20995284")

async def setup(bot: commands.Bot) -> None:
	settings = bot.get_cog("Settings")
	await bot.add_cog(Bonk(bot, settings))