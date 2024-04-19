# Credits CorpNewt for 
# https://github.com/corpnewt/CorpBot.py/blob/bc5c08e848a766d5c75920352b0a09bc4c04c2b2/Cogs/Actions.py

from Utils import Member
from Utils import Computer
import discord
from discord.ext import commands

class Boop(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.command()
	async def boop(self, ctx, member=None):
		"""
		[object]
		boops an object
		"""

		Bot = self.bot.user.id
		M = Member.member()
		C = Computer.computer()

		nothingList = [ 'you stretch out your hand in the air, but there\'s nothing there...',
						'you try and find someone to boop, but there\'s no one there.',
						'you look around the channel for someone to boop.',
						'you eye all the heads in the room, just waiting to be booped.',
						'are you sure you have someone to boop?',
						'I get it. You want to boop *someone*.']

		selfList = [	'you boop yourself on the nose with your finger.',
						'you try to boop your head, but your hand gets lost along the way.',
						'you happily boop yourself, but you are now very giddy.',
						'wait - are you sure you want to boop yourself?',
						'you might not be the smartest...',
						'you might have some issues.',
						'you try to boop yourself.',
						'why would you boop yourself?']

		memberList = [  'you outstretch your lucky finger and boop *{}* in one go.',
						'you try to boop *{}*, but you just can\'t quite do it - you miss their head, the taste of failure hanging stuck to your hand...',
						'you sneak a boop onto *{}*.  They probably didn\'t even notice.',
						'you poke your hand onto *{}\'s* hand - You run away as they run after you.',
						'you happily drum your fingers away - *{}* starts to look annoyed.',
						'you\'re feeling boopy - *{}* sacrifices themself involuntarily.',
						'somehow you end up booping *{}*.',
						'you climb *{}*\'s head and  use it as a bouncy castle... they feel amused.']
		
		itemList = [	'you put your hand onto *{}*\'s head. *Bliss.*',
						'your hand touches *{}*\'s snoot - it feels satisfying.',
						'you happily boop *{}*, it\'s lovely!',
						'you just can\'t bring yourself to boop *{}* - so you just let your hand linger...',
						'you attempt to boop *{}*, but you\'re clumsier than you remember - and fail...',
						'you boop *{}*.',
						'*{}* feels annoyed from your booping.',
						'*{}* starts resembling a happy pupper.']
		
		if member:
			m = M.displayName(ctx, member)
			if m == None:
				msg = C.text(ctx, itemList, member)
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
	await bot.add_cog(Boop(bot))