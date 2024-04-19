# Credits CorpNewt for 
# https://github.com/corpnewt/CorpBot.py/blob/bc5c08e848a766d5c75920352b0a09bc4c04c2b2/Cogs/Actions.py

import random
import discord
from discord.ext import commands
from Utils import Member
from Utils import Computer

class Drink(commands.Cog):
	def __init__(self, bot, settings):
		self.bot = bot
		self.settings = settings

	@commands.command()
	async def drink(self, ctx, member=None):
		"""
		[Thing]
		Drinks something
		"""
			
		Bot = self.bot.user.id
		M = Member.member()
		C = Computer.computer()

		nothingList = [ 'you stare at your glass full of *nothing*...',
						'that cup must\'ve had something in it, so you drink *nothing*...',
						'you should probably just go get a drink.',
						'that desk looks pretty empty',
						'are you sure you know what drinking is?',
						'you desperatly search for something to drink']
		
		botList = [ 	'you try to drink *me*, but I dodge your straw.',
						'You search for me, only to realise that *I* am already drinking you!',
						'I\'m a bot.  You can\'t drink me.',
						'you stick a straw in... wait... in nothing, because I\'m *digital!*.',
						'what do you think I am to let you drink me?',
						'I don\'t think you would like the taste of me.',
						'you can\'t drink me, I\'m a machine!']
		
		selfList = [	'you stab yourself with a straw - not surprisingly, it hurts.',
						'you fit yourself in to a cup, but you just can\'t do it.',
						'you happily drink away, but you are now very floppy.',
						'wait - you\'re not a drink!',
						'you might not be the smartest...',
						'you might have some issues.',
						'you try to drink yourself.',
						'why would you drink yourself?']
		
		memberList = [  'you grab your lucky straw and empty *{}* in one sip.',
						'you try to drink *{}*, but you just can\'t quite do it - you spit them out, the taste of failure hanging in your mouth...',
						'you drink a small sip of *{}*.  They probably didn\'t even notice.',
						'you stab your straw into *{}\'s* shoulder - You run away as they run after you.',
						'you happily drink away - *{}* starts to look like an empty Capri Sun package.',
						'you are thirsty - *{}* sacrifices themself involuntarily.',
						'somehow you end up emptying *{}*.']
		
		itemList = [	'you take a big sip of *{}*. *Delicious.*',
						'your straw sinks into *{}* - it tastes satisfying.',
						'you thirstly guzzle *{}*, it\'s lovely!',
						'you just can\'t bring yourself to drink *{}* - so you just hold it for awhile...',
						'you attempt to drain *{}*, but you\'re clumsier than you remember - and fail...',
						'you drink *{}*.',
						'*{}* dries up from your drinking.',
						'*{}* starts resembling the Aral Sea.']

		if member:
			m = M.displayName(ctx, member)
			if m == None:
				msg = C.text(ctx, itemList, member)
			elif m.id == Bot:
				msg = C.text(ctx, botList)
			elif m.id == ctx.author.id:
				msg = C.text(ctx, selfList)
			else:
				msg = C.text(ctx, memberList, m.name)
		else:
			msg = C.text(ctx, nothingList)

		# print(msg)
		await ctx.send(msg)

async def setup(bot: commands.Bot) -> None:
	settings = bot.get_cog("Settings")
	await bot.add_cog(Drink(bot, settings))