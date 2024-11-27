# Credits CorpNewt for 
# https://github.com/corpnewt/CorpBot.py/blob/bc5c08e848a766d5c75920352b0a09bc4c04c2b2/Cogs/Actions.py

import random
import discord
from discord.ext import commands
from Utils import Member
from Utils import Computer

class HighFive(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.command()
	async def highfive(self, ctx, member=None):
		"""
		[object]
		High fives a object
		"""
			
		Bot = self.bot.user.id
		M = Member.member()
		C = Computer.computer()
		
		nothingList = [ 'you stand alone for an eternity, hand raised up - desperate for any sort of recognition...',
						'with a wild swing you throw your hand forward - the momentum carries you to the ground and you just lay there - high fiveless...',
						'the only sound you hear as a soft *whoosh* as your hand connects with nothing...']
		
		botList = [ 	'the sky erupts with 1\'s and 0\'s as our hands meet in an epic high five of glory!',
						'you beam up to the cloud and receive a quick high five from me before downloading back to Earth.',
						'I unleash a fork-bomb of high five processes!',
						'01001000011010010110011101101000001000000100011001101001011101100110010100100001']
		
		
		selfList = [	'ahh - high fiving yourself, classy...',
						'that\'s uh... that\'s just clapping...',
						'you run in a large circle - *totally* high fiving all your friends...',
						'now you\'re at both ends of a high five!']
		
		memberList = [  'you and *{}* jump up for an epic high five - freeze-framing as the credits roll and some wicked 80s synth plays out.',
						'you and *{}* elevate to a higher plane of existence in wake of that tremendous high five!',
						'a 2 hour, 3 episode anime-esque fight scene unfolds as you and *{}* engage in a world-ending high five!',
						'it *was* tomorrow - before you and *{}* high fived with enough force to spin the Earth in reverse!',
						'like two righteous torpedoes - you and *{}* connect palms, subsequently deafening everyone in a 300-mile radius!']
		
		itemList = [	'neat... you just high fived *{}*.',
						'your hand flops through the air - hitting *{}* with a soft thud.',
						'you reach out a hand, gently pressing your palm to *{}*.  A soft *"high five"* escapes your lips as a tear runs down your cheek...',
						'like an open-handed piston of ferocity - you drive your palm into *{}*.']

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
	bot.add_cog(HighFive(bot))