# Credits CorpNewt for 
# https://github.com/corpnewt/CorpBot.py/blob/bc5c08e848a766d5c75920352b0a09bc4c04c2b2/Cogs/Actions.py
# used the Action lines

import random
import discord
from discord.ext import commands
from Utils import Member
from Utils import Computer

class Eat(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.command()
	async def eat(self, ctx, member=None):
		"""Eats something"""
		Bot = self.bot.user.id
		M = Member.member()
		C = Computer.computer()

		nothingList = [ 'you sit quietly and eat *nothing*...',
					'you\'re *sure* there was something to eat, so you just chew on nothingness...',
					'there comes a time when you need to realize that you\'re just chewing nothing for the sake of chewing.  That time is now.']
		
		botList = [ 'you try to eat *me* - but unfortunately, I saw it coming - your jaw hangs open as I deftly sidestep.',
					'your mouth hangs open for a brief second before you realize that *I\'m* eating *you*.',
					'I\'m a bot.  You can\'t eat me.',
					'your jaw clamps down on... wait... on nothing, because I\'m *digital!*.',
					'what kind of bot would I be if I let you eat me?']
		
		selfList = ['you clamp down on your own forearm - not surprisingly, it hurts.',
					'you place a finger into your mouth, but *just can\'t* force yourself to bite down.',
					'you happily munch away, but can now only wave with your left hand.',
					'wait - you\'re not a sandwich!',
					'you might not be the smartest...']
		
		memberList = [  'you unhinge your jaw and consume *{}* in one bite.',
						'you try to eat *{}*, but you just can\'t quite do it - you spit them out, the taste of failure hanging in your mouth...',
						'you take a quick bite out of *{}*.  They probably didn\'t even notice.',
						'you sink your teeth into *{}\'s* shoulder - they turn to face you, eyes wide as you try your best to scurry away and hide.',
						'your jaw clamps down on *{}* - a satisfying *crunch* emanates as you finish your newest meal.']
		
		itemList = [ 	'you take a big chunk out of *{}*. *Delicious.*',
						'your teeth sink into *{}* - it tastes satisfying.',
						'you rip hungrily into *{}*, tearing it to bits!',
						'you just can\'t bring yourself to eat *{}* - so you just hold it for awhile...',
						'you attempt to bite into *{}*, but you\'re clumsier than you remember - and fail...']

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


def setup(bot):
	bot.add_cog(Eat(bot))