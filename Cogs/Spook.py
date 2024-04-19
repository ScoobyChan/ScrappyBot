# Credits CorpNewt for 
# https://github.com/corpnewt/CorpBot.py/blob/bc5c08e848a766d5c75920352b0a09bc4c04c2b2/Cogs/Actions.py

import random
import discord
from discord.ext import commands
from Utils import Member
from Utils import Computer

class Spook(commands.Cog):
	def __init__(self, bot, settings):
		"""Credits to CorpNewt for Computer and Member"""
		self.bot = bot
		self.settings = settings

	@commands.command()
	async def spook(self, ctx, member=None):
		"""
		[object]
		Spooks and object
		"""

		Bot = self.bot.user.id
		M = Member.member()
		C = Computer.computer()

		nothingList = [ 'you spook no one but yourself',
						'you spook nothing, sp00py...',
						'sadly, no one got spooked',
						'it is sp00... you can\t spook air']
		botList = [ 	'you scared the living pumpkin out of me!',
						'you spooked me so hard, I got the Heebie-jeebies...', # https://www.myenglishteacher.eu/blog/idioms-for-being-afraid/
						'you sp00p me? But I\'m a bot... I can\'t be spooked!',
						'sorry, but I cannot let you spook me; My digital emotions will get all messed up!'
						'aaaaaaaaaah! Don\t you scare me like that again!']
		selfList = [	'go watch a scary movie to be absolutely sp00ped!',
						'boo! Did you scare you?',
						'you look yourself in the mirror and get a little scared...',
						'get spooked by... yourself?',
						'sp00py, but why spook yourself?']
		memberList = [  'you sp00p *{}* so hard that they start screaming!',
						'you tried to sneak up on *{}*, but they heard you sneakin\' and fail...',
						'it is sp00py time! Hey *{}*, boo!',
						'congrats, *{}* dun sp00ked.',
						'get spook3d *{}*!']
		
		itemList = [	'you spook *{}* with no reaction, leaving you looking weird...',
						'*{}* got sp00p3d so hard, it ran away!',
						'you trick or treat *{}* without any reaction...',
						'you do your best to sp00p *{}*, but fail...',
						'sp00py time! *{}* gets sp00ped harder than you thought and starts crying!']

		if member:
			m = M.displayName(ctx, member)
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

async def setup(bot: commands.Bot) -> None:
	settings = bot.get_cog("Settings")
	await bot.add_cog(Spook(bot, settings))