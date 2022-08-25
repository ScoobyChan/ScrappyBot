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
		item = 'Test'
		# print(await self.fuzSearch(ctx, search, my_list))
		sel = await self.fuzSelect(ctx, item, my_list)
		print(sel)
		 
	async def fuzSearch(self, ctx, Search, List):		
		
		if not isinstance(List, list): 
			return await ctx.send('please input a list')


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
	
	async def fuzSelect(self, ctx, _item, _title):				
		print(len(_title))
		max_num = 5
		min_num = 0
		_sent = False
		choice = None

		_joined_list = ''
		num = page = page_total = 1
		for x in _title[min_num:max_num]:
			_joined_list += '{} - {}\n'.format(num, x)
			num += 1

			
		if ctx.author.top_role.colour:
			col = ctx.author.top_role.colour
		else:
			col =self.settings.randomColor()
		
		page_total = len(_title)
		if (page_total / 5) > (page_total // 5):
			page_total = (page_total // 5) + 1

		embed = discord.Embed(title="{} Selector".format(_item), colour=col)
		embed.description = _joined_list
		embed.set_footer(text="{}/{}".format(page, page_total))
		msg = await ctx.send(embed=embed)

		while True:
			if not _sent:
				_sent = True				
			else:
				_joined_list = ''
				num = 1
				for x in _title[min_num:max_num]:
					_joined_list += '{} - {}\n'.format(num, x)
					num += 1

				embed = discord.Embed(title="{} Selector".format(_item), colour=col)
				embed.description = _joined_list
				embed.set_footer(text="{}/{}".format(page, page_total))
				await msg.edit(embed=embed)
				await msg.clear_reactions() 
			
			try:
				await asyncio.sleep(0.05)

				if len(_title) > 5: await msg.add_reaction("⬅️")
				if len(_title[min_num:max_num]) >= 1: await msg.add_reaction("\N{DIGIT ONE}\N{COMBINING ENCLOSING KEYCAP}")
				if len(_title[min_num:max_num]) >= 2: await msg.add_reaction('\N{DIGIT TWO}\N{COMBINING ENCLOSING KEYCAP}')
				if len(_title[min_num:max_num]) >= 3: await msg.add_reaction('\N{DIGIT THREE}\N{COMBINING ENCLOSING KEYCAP}')
				if len(_title[min_num:max_num]) >= 4: await msg.add_reaction('\N{DIGIT FOUR}\N{COMBINING ENCLOSING KEYCAP}')
				if len(_title[min_num:max_num]) >= 5: await msg.add_reaction('\N{DIGIT FIVE}\N{COMBINING ENCLOSING KEYCAP}')
				if len(_title) > 5: await msg.add_reaction("➡️")

				await msg.add_reaction('🚫')
				
				def check(reaction: discord.Reaction, adder: discord.User) -> bool:
					return adder == ctx.message.author and reaction.message.id == msg.id

				reaction, adder = await self.bot.wait_for('reaction_add', timeout=30, check=check)
				#timeout= 30
				if reaction.emoji == '⬅️' and len(_title) > 5:
					print(min_num - 5)
					if (min_num - 5) >= 0:
						max_num -= 5
						min_num -= 5
						page -= 1
						print('Previous')

				elif reaction.emoji == '1⃣' and len(_title[min_num:max_num]) >= 1:
					choice = 0 + min_num
					print(choice)
					break

				elif reaction.emoji == '2⃣' and len(_title[min_num:max_num]) >= 2:
					choice = 1 + min_num
					break

				elif reaction.emoji == '3⃣' and len(_title[min_num:max_num]) >= 3:
					choice = 2 + min_num
					break

				elif reaction.emoji == '4⃣' and len(_title[min_num:max_num]) >= 4:
					choice = 3 + min_num
					break

				elif reaction.emoji == '5⃣' and len(_title[min_num:max_num]) >= 5:
					choice = 4 + min_num
					break

				elif reaction.emoji == '➡️' and len(_title) > 5:
					print((max_num + 5) // 5) 
					print((len(_title) // 5) + 1)
					
					if ((max_num) // 5) != ((len(_title) // 5) + 1):
						max_num += 5
						min_num += 5
						page += 1
						print('Next')

				elif reaction.emoji == '🚫':
					break
			
			except asyncio.exceptions.TimeoutError:
				break
		
		await msg.clear_reactions() 
		print(choice)
		return (choice)
				
	async def fuzList(self, ctx, _item, _title, max_num = 5):				
		if not isinstance(_item, list) and not isinstance(_item, dict): 
			return await ctx.send('please input a list')

		min_num = 0
		_sent = False

		_joined_list = ''
		num = page = page_total = 1

		if isinstance(_item, list):
			for x in _item[min_num:max_num]:
				_joined_list += '{} - {}\n'.format(num, x)
				num += 1
		else:
			item_list = []
			for x in _item:
				item_list.append(x)
			
			for x in item_list[min_num:max_num]:				
				_joined_list += '{} - {}({})\n'.format(num, _item[x]['Name'], x)
				num += 1

		page_total = len(item_list)
		if (page_total / max_num) > (page_total // max_num):
			page_total = (page_total // max_num) + 1
			
		if ctx.author.top_role.colour:
			col = ctx.author.top_role.colour
		else:
			col =self.settings.randomColor()
			
		embed = discord.Embed(title="{} Selector".format(_item), colour=col)
		embed.description = _joined_list
		embed.set_footer(text="{}/{}".format(page, page_total))
		msg = await ctx.send(embed=embed)

		while True:
			if not _sent:
				_sent = True				
			else:
				_joined_list = ''
				num = 1
				if isinstance(_item, list):
					for x in _title[min_num:max_num]:
						_joined_list += '{} - {}\n'.format(num, x)
						num += 1
				else:
					for x in item_list[min_num:max_num]:	
						_joined_list += '{} - {}({})\n'.format(num, _title[x]['Name'], x)
						num += 1

				embed = discord.Embed(title="{} Selector".format(_item), colour=col)
				embed.description = _joined_list
				embed.set_footer(text="{}/{}".format(page, page_total))
				await msg.edit(embed=embed)
				await msg.clear_reactions() 
			
			try:
				await asyncio.sleep(0.05)

				if len(_title) > 5: await msg.add_reaction("⬅️")
				if len(_title) > 5: await msg.add_reaction("➡️")

				await msg.add_reaction('🚫')
				
				def check(reaction: discord.Reaction, adder: discord.User) -> bool:
					return adder == ctx.message.author and reaction.message.id == msg.id

				reaction, adder = await self.bot.wait_for('reaction_add', timeout=30, check=check)
				#timeout= 30
				if reaction.emoji == '⬅️' and len(_title) > 5:
					print(min_num - 5)
					if (min_num - 5) >= 0:
						max_num -= 5
						min_num -= 5
						page -= 1
						print('Previous')

				elif reaction.emoji == '➡️' and len(_title) > 5:
					print((max_num + 5) // 5) 
					print((len(_title) // 5) + 1)
					if ((max_num) // 5) != (len(_title) // 5) + 1:
						max_num += 5
						min_num += 5
						page += 1
						print('Next')

				elif reaction.emoji == '🚫':
					await msg.clear_reactions() 
					break
			
			except asyncio.exceptions.TimeoutError:
				break	
		

def setup(bot):
	settings = bot.get_cog("Settings")
	bot.add_cog(FuzzySearch(bot, settings))