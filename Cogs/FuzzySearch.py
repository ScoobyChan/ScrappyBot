import json
import os
import discord
from discord.utils import get
from discord.ext import commands
from collections import Counter
import asyncio

from Utils import Utils

class FuzzySearch(commands.Cog):
	def __init__(self, bot, settings):
		self.bot = bot
		self.settings = settings
		self.Utils = Utils.Utils()

	# Combine search and select together

	@commands.command()
	async def fuzzSearchtest(self, ctx):
		"""
		Tests the fuzzy search function but I need to re make it
		"""

		my_list = ["geeks", "geeg", "keegs", "geek", "skeeg", "keegs", "practice", "aa"] 
		search = "eegsk"
		print(await self.fuzSearch(ctx, search, my_list))
		 
	async def fuzSearch(self, ctx, Search, List):		
		_title = list(filter(lambda x: (Counter(x) == Counter(Search)), List))
		
		num = 0
		cap = 4
		sel = ''
		for t in _title[:5]:
			num += 1
			sel += (f"\n{num} - {t}")
			if num == 3: break

		# print(sel)

		# await ctx.send(f'**Top Selected**\n*HINT - press react to choose*\n```md\n{sel}\n```') ## Before react
		col = ctx.author.top_role.colour
		embed = self.Utils.embed({"title":"Top Selected", "desc":sel, "color":col})		
		msg = await ctx.send(embed=embed)
		
		if len(_title) >= 1:
			await msg.add_reaction("\N{DIGIT ONE}\N{COMBINING ENCLOSING KEYCAP}")
		if len(_title) >= 2:
			await msg.add_reaction('\N{DIGIT TWO}\N{COMBINING ENCLOSING KEYCAP}')
		if len(_title) >= 3:
			await msg.add_reaction('\N{DIGIT THREE}\N{COMBINING ENCLOSING KEYCAP}')
		if len(_title) >= 4:
			await msg.add_reaction('\N{DIGIT FOUR}\N{COMBINING ENCLOSING KEYCAP}')
		if len(_title) >= 5:
			await msg.add_reaction('\N{DIGIT FIVE}\N{COMBINING ENCLOSING KEYCAP}')
		await msg.add_reaction('🚫')

		def check(reaction: discord.Reaction, adder: discord.User) -> bool:
			return adder == ctx.message.author and reaction.message.id == msg.id

		reaction, adder = await self.bot.wait_for('reaction_add', check=check)

		if reaction.emoji == '1⃣':
			choice = 0

		elif reaction.emoji == '2⃣':
			choice = 1

		elif reaction.emoji == '3⃣':
			choice = 2

		elif reaction.emoji == '4⃣':
			choice = 3

		elif reaction.emoji == '5⃣':
			choice = 4

		elif reaction.emoji == '🚫':
			await msg.delete()  
			await ctx.send('Search has been cancelled')
			return False

		await msg.delete()  
		# await ctx.send(f'You have Selected: **{_title[choice]}**')
		return _title[choice]
	
	async def fuzSelect(self, ctx, _title):
		cap = 4
		num = 0
		sel = ''
		for t in _title[:5]:
			num += 1
			sel += (f"\n{num}  - {t}")

		# await ctx.send(f'**Top Selected**\n*HINT - press react to choose*\n```md\n{sel}\n```') ## Before react
		col = ctx.author.top_role.colour
		embed = self.Utils.embed({"title":"Top Selected", "desc":sel, "color":col})		
		msg = await ctx.send(embed=embed)
		
		if len(_title[:5]) >= 1:
			await msg.add_reaction("\N{DIGIT ONE}\N{COMBINING ENCLOSING KEYCAP}")
		if len(_title[:5]) >= 2:
			await msg.add_reaction('\N{DIGIT TWO}\N{COMBINING ENCLOSING KEYCAP}')
		if len(_title[:5]) >= 3:
			await msg.add_reaction('\N{DIGIT THREE}\N{COMBINING ENCLOSING KEYCAP}')
		if len(_title[:5]) >= 4:
			await msg.add_reaction('\N{DIGIT FOUR}\N{COMBINING ENCLOSING KEYCAP}')
		if len(_title[:5]) >= 5:
			await msg.add_reaction('\N{DIGIT FIVE}\N{COMBINING ENCLOSING KEYCAP}')
		await msg.add_reaction('🚫')

		def check(reaction: discord.Reaction, adder: discord.User) -> bool:
			return adder == ctx.message.author and reaction.message.id == msg.id

		reaction, adder = await self.bot.wait_for('reaction_add', check=check)

		if reaction.emoji == '1⃣':
			choice = 0

		elif reaction.emoji == '2⃣':
			choice = 1

		elif reaction.emoji == '3⃣':
			choice = 2

		elif reaction.emoji == '4⃣':
			choice = 3

		elif reaction.emoji == '5⃣':
			choice = 4

		elif reaction.emoji == '🚫':
			await msg.delete()  
			await ctx.send('Search has been cancelled')
			return False

		await msg.delete()  
		# await ctx.send(f'You have Selected: **{_title[choice]}**')
		return _title[choice]

def setup(bot):
	settings = bot.get_cog("Settings")
	bot.add_cog(FuzzySearch(bot, settings))